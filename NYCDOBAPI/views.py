from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from .serializers import PropertySerializer, PropertyCreateSerializer, AdditionalContactSerializer
from .serializers import ContactSerializer, PriceSerializer, UserDetailsSerializers, ProfileForUserDataSerializer, ComplaintsSerializers, VoilationsSerializer, OTPSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from main.models import AdditionalContact, Profile, UserCredsSaver
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404
from main.models import User, Property, Price, Complaints, Voilation
from django.conf import settings
from django.template.loader import get_template

from django.core.mail import EmailMultiAlternatives, EmailMessage
import random


# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)




class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        user = authenticate(request, **request.data)
        if user is None:
            return Response({'error': 'Invalid login credentials'}, status=400)
        # Create access and refresh tokens for the user
        if Profile.objects.filter(user=user).first().is_verified:
            token = get_tokens_for_user(user)
            # Get the user's orders
            user_id = user.id
            user_for_data = User.objects.get(id=user_id)
            user_profile = Profile.objects.filter(user=user_for_data).first()
            user_property = Property.objects.filter(
                user=user_for_data)
            user_a_contacts = AdditionalContact.objects.filter(
                user=user_for_data)
            user_data = UserDetailsSerializers(user_for_data, many=False)
            user_properties = PropertySerializer(user_property, many=True)
            user_additional_contacts = AdditionalContactSerializer(user_a_contacts, many=True)

            user_profile = ProfileForUserDataSerializer(
                user_profile, many=False)
            return Response({'msg': 'Login Success', 'user': user_data.data, 'user_profile': user_profile.data, 'Properties': user_properties.data, 'additional_contacts':user_additional_contacts.data,  'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email is not verified'}, status=400)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)



class VerifyRegisteration(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):

        try:
            data = request.data
            serializer = OTPSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                
                otp = serializer.data['otp']
                

                profile_obj = Profile.objects.get(auth_token=otp)

                if profile_obj:
                    if profile_obj.is_verified:
                        return Response({'msg': 'Account is already verified'}, status=status.HTTP_200_OK)
                    else:
                        profile_obj.is_verified = True
                        profile_obj.auth_token = str(random.randint(11111111, 99999999))
                        profile_obj.save()
                        
                        subject = 'Welcome to 311Alert'
                        user = profile_obj.user
                        fname = user.first_name
                        usercreds = UserCredsSaver.objects.get(user=user)
                        email = usercreds.email
                        password = usercreds.password
                        context = {
                            "fname": fname,
                            "password": password,
                            "email": email
                        }
                        # print(context)

                        from_email = settings.EMAIL_HOST_USER

                        templ = get_template('welcometemplate.txt')
                        messageing = templ.render(context)
                        emailnew = EmailMultiAlternatives(
                            subject, messageing, from_email, [ user.email])

                        emailnew.content_subtype = 'html'
                        emailnew.send()

                        
                        return Response({'msg': 'Account verified successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'Invalid Url !!!'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'msg': 'Varification fialed or already varified !!!'}, status=status.HTTP_400_BAD_REQUEST)


class ComplaintsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        complaints = Complaints.objects.filter(user=user)
        serializer = ComplaintsSerializers(
            complaints, many=True)
        return Response({'msg': serializer.data}, status=status.HTTP_200_OK)


class VoilationsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        voilations = Voilation.objects.filter(user=user)
        serializer = VoilationsSerializer(voilations, many=True)
        return Response({'msg': serializer.data}, status=status.HTTP_200_OK)


class PropertyListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        properties = Property.objects.filter(user=user)
        serializer = PropertySerializer(properties, many=True)
        return Response({'msg': serializer.data}, status=status.HTTP_200_OK)


class PropertyView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PropertyCreateSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'Property added  Successful'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        serializer = PropertyCreateSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'Property edited  Successful'}, status=status.HTTP_201_CREATED)


class PropertyDeleteView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, property_id):
        serializer = PropertySerializer()
        try:
            Property.objects.get(id=property_id).delete()
            return Response({'msg': 'Property Deleted'}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'msg': 'unexpected Error Occured'}, status=status.HTTP_201_CREATED)






class AdditionalContactsListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        a_contacts = AdditionalContact.objects.filter(user=user)
        serializer = AdditionalContactSerializer(a_contacts, many=True)
        return Response({'msg': serializer.data}, status=status.HTTP_200_OK)


class AdditionalContactView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AdditionalContactSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        

        return Response({'msg': 'Additional Contact added  Successful'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        serializer = AdditionalContactSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'Additional Contact edited  Successful'}, status=status.HTTP_201_CREATED)


class AdditionalContactDeleteView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, a_c_id):
        serializer = AdditionalContactSerializer()
        try:
            AdditionalContact.objects.get(id=a_c_id).delete()
            return Response({'msg': 'Additional Contact Deleted'}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'msg': 'unexpected Error Occured'}, status=status.HTTP_201_CREATED)




class PriceView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        prices = Price.objects.all()
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Message Sent Successful'}, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, profile_id, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # user = get_object_or_404(User, user=request.user)
        # print(user)
        profile = Profile.objects.get(id=profile_id)
        print(self.request.user)
        profile.can_add = serializer.data['can_add']
        profile.is_pro = serializer.data['is_pro']
        profile.profile_image = serializer.data['profile_image']
        profile.is_yearly = serializer.data['is_yearly']
        profile. pro_start_date = serializer.data['pro_start_date']
        profile. strip_costumer_token = serializer.data['strip_costumer_token']
        profile. strip_subscription_token = serializer.data['strip_subscription_token']
        profile.save()

        return Response({'msg': 'profile Updated Successful'}, status=status.HTTP_201_CREATED)
