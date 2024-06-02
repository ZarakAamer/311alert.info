from rest_framework import serializers
from main.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from main.models import Userpayments, UserCredsSaver
from main.models import Price
from main.models import Profile
from main.models import Contact
from main.models import Complaints
from main.models import Voilation
from main.models import HPDComplaints
from main.models import HPDViolations
from main.models import HPDCharges
from main.models import HPDLitigation
from main.models import HPDRepair
from main.models import HPDBedBugReport
from main.models import Property, AdditionalContact
from main.models import Ticket, TicketReply
import uuid

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

import random


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'phone',
                  'company_name', 'address', 'city',  'state',  'zip',  'cell', 'our_source']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')

        if not password:
            raise serializers.ValidationError("Password is necessary")
        return attrs

    def create(self, validate_data):
        user = User.objects.create_user(**validate_data)
        fname = user.first_name
        email = user.email
        auth_token = str(random.randint(11111111, 99999999))
        Profile.objects.create(user=user, auth_token=auth_token)

        Userpayments.objects.create(user=user)
        UserCredsSaver.objects.create(
            user=user, email=email, password=validate_data["password"])

        subject = 'Your accounts need to be verified'

        link = auth_token

        context = {
            "link": link,
            "fname": fname,
        }

        from_email = settings.EMAIL_HOST_USER
        print("printed")

        templ = get_template('templetext.txt')
        messageing = templ.render(context)
        # print(messageing)

        emailnew = EmailMultiAlternatives(
            subject, messageing,  from_email, [email])

        emailnew.content_subtype = 'html'
        emailnew.send()

        return user


class ProfileForUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField()

    class Meta:
        fields = ['otp']


class UserDetailsSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']


class UserWithIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    userdata = UserDetailsSerializers(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password',  'userdata']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = Profile.objects.get(user=user).auth_token
            link = token
            body = 'Following is your password reset code ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField()

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')

            token = attrs.get('token')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
            profile = Profile.objects.get(auth_token=token)
            user = profile.user
            user.set_password(password)
            profile.auth_token = str(random.randint(11111111, 99999999))
            user.save()
            return attrs
        except:

            raise serializers.ValidationError('Token is not Valid or Expired')


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyCreateSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(max_length=100)
    zip = serializers.CharField(max_length=100)
    borough = serializers.CharField(max_length=200)
    block = serializers.CharField(max_length=100)
    lott = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    house = serializers.CharField(max_length=100)
    bin_number = serializers.CharField(max_length=200)

    def create(self, validated_data):
        user = self.context.get('user')
        property_name = validated_data['property_name']
        zip = validated_data['zip']
        borough = validated_data['borough']
        block = validated_data['block']
        lott = validated_data['lott']
        street = validated_data['street']
        house = validated_data['house']
        bin_number = validated_data['bin_number']

        # product = Product.objects.get(id=int(product_id))

        property = Property.objects.create(user=user,  property_name=property_name, zip=zip,
                                           borough=borough, block=block, lott=lott, street=street, house=house, bin_number=bin_number)

        return property

    class Meta:
        model = Property
        fields = [
            'property_name',
            'zip',
            'borough',
            'block',
            'lott',
            'street',
            'house',
            'bin_number'
        ]


class ComplaintsSerializers(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = Complaints
        fields = '__all__'


class VoilationsSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = Voilation
        fields = '__all__'


class HPDComplaintsSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = HPDComplaints
        fields = '__all__'


class HPDViolationsSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = HPDViolations
        fields = '__all__'


class HPDChargesSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = HPDCharges
        fields = '__all__'


class HPDLitigationSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = HPDLitigation
        fields = '__all__'


class HPDRepairSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = HPDRepair
        fields = '__all__'


class HPDBedBugReportSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = UserDetailsSerializers()

    class Meta:
        model = HPDBedBugReport
        fields = '__all__'


class PropertyWithIdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Property
        fields = ['id']


class AdditionalContactSerializer(serializers.ModelSerializer):
    property = PropertyWithIdSerializer()
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)

    def create(self, validated_data):

        user = self.context.get('user')
        # property = validated_data['property']
        property_data = validated_data.pop('property')
        property = Property.objects.get(id=property_data['id'])
        print(property)
        email = validated_data['email']
        name = validated_data['name']
        phone = validated_data['phone']

        a_contacts = AdditionalContact.objects.create(
            user=user, property=property, email=email, name=name, phone=phone)

        return a_contacts

    class Meta:
        model = AdditionalContact
        fields = ['property', 'email', 'phone', 'name']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    can_add = serializers.IntegerField()
    profile_image = serializers.ImageField()
    is_pro = serializers.BooleanField()
    is_yearly = serializers.BooleanField()
    pro_start_date = serializers.DateField()
    strip_costumer_token = serializers.CharField(max_length=200)
    strip_subscription_token = serializers.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = ['can_add',  'profile_image', 'is_pro', 'is_yearly',
                  'pro_start_date', 'strip_costumer_token', 'strip_subscription_token']
