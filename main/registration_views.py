from django.shortcuts import render, redirect
import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Profile, Property
import stripe
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User, UserCredsSaver, Userpayments
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import random


def login_attempt(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()

        if user is None:
            messages.error(request, "User doesn't exist.")
            return redirect('login')

        user = authenticate(email=email, password=password)

        if user is None:

            messages.error(request, "Password Wrong!.")
            forget = True
            return render(request, 'login.html',  {"forget": forget})

        profile_obj = Profile.objects.filter(user=user).first()
        if not profile_obj.is_verified:
            messages.success(
                request, 'Email is not verified check your email inbox.')
            return redirect('login')
        else:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            company = request.POST.get('cname')
            address_first = request.POST.get('address_first')
            address_second = request.POST.get('address_second')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            phone = request.POST.get('phone')
            fax = request.POST.get('fax')
            cell = request.POST.get('cell')
            our_source = request.POST.get('our_source')
            account_type = request.POST.get('account_type')
            username = fname+state+email

            user = User.objects.filter(email=email)
            usern = User.objects.filter(username=username)
            if user or usern:
                messages.warning(
                    request, 'User already exists.')
                return redirect('register')
            else:
                messages.success(
                    request, 'User Created successfuly.')
                addresses = address_first + ' ' + address_second

                user = User(email=email, username=username, first_name=fname, last_name=lname, phone=phone, company_name=company,
                            address=addresses, city=city, state=state, zip=zip, fax=fax, cell=cell, our_source=our_source,)
                user.set_password(password)
                user.save()
                user_id = user.id
                UserCredsSaver.objects.create(
                    user=user, email=email, password=password)

                login(request, user)
                auth_token = str(random.randint(11111111, 99999999))
                profile_obj = Profile.objects.create(
                    user=user, auth_token=auth_token)
                profile_obj.save()
                logout(request)

                send_mail_after_registration(
                    email=email, auth_token=auth_token, fname=fname)
                messages.success(
                    request, 'Check your email for verification code')
                return redirect("verify_email")

    return render(request, 'register.html')

@login_required
def user_prof(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    properties = Property.objects.filter(user=user)

    property_consumed = int(properties.count())/int(profile.can_add)*100
    context = {
        "user": user,
        "profile": profile,
        "properties": properties,
        "property_consumed": int(property_consumed),
    }
    return render(request, 'user_prof.html', context)


def verify_email(request):
    return render(request, 'verifyEmail.html')


@ login_required(login_url='login')
def edit_user_information(request):
    return render(request, 'edit_user_information.html')


def change_profile_image(request):
    user = request.user
    if request.method == 'POST':
        p_image = request.FILES.get('profile_picture')
        print(f"This is the image uploaded right now {p_image} ")
        profile = Profile.objects.filter(user=user).first()

        profile.profile_image = p_image
        profile.save()
        messages.success(request, 'Profile image changed successfully!')
        return redirect('user_prof')

    else:

        return render(request, 'user_prof.html')


@ login_required(login_url='login')
def update_profile_info(request):
    user = request.user
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if fname == '':
            pass
        else:
            user.first_name = fname

        if lname == '':
            pass
        else:
            user.last_name = lname

        if phone == '':
            pass
        else:
            user.phone = phone

        if email == '':
            pass
        else:
            user.email = email

        if address == '':
            pass
        else:
            user.address = address

        user.save()

        messages.success(request, 'Your account is updated!')
        return redirect('user_prof')


@ login_required(login_url='login')
def update_password_info(request):

    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('confirm_password')
            if password != password2:

                messages.warning(
                    request, "Password and confirm password do not macth")
                return redirect('edit_user_information')
            else:
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password changed! ')

                return redirect('edit_user_information')
        else:
            return redirect('edit_user_information')
    else:
        return redirect('edit_user_information')


def verify(request):
    if request.method == 'POST':
        try:
            auth_token = request.POST.get("auth_token")
            profile_obj = Profile.objects.filter(auth_token=auth_token).first()

            if profile_obj:
                user = profile_obj.user

                # email verified send email
                verified_email(user)

                if profile_obj.is_verified:
                    messages.success(
                        request, 'Your account is already verified.')
                    if profile_obj.is_pro:
                        return redirect('login')
                    else:
                        return redirect('payment_after_registeration', param1=user.id)
                profile_obj.is_verified = True
                profile_obj.auth_token = str(
                    random.randint(11111111, 99999999))
                profile_obj.save()
                messages.success(request, 'Your account has been verified.')
                return redirect('payment_after_registeration', param1=user.id)

            else:
                messages.success(
                    request, 'Invalid url try again or contact support team.')
                return redirect('login')
        except Exception as e:
            print(e)
            return redirect('home')
    else:
        return redirect('/')


def ChangePassword(request, auth_token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/password-reset-verification/{auth_token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/password-reset-verification/{auth_token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password Changed Successfully.')

            return redirect('login')

    except Exception as e:
        print(e)
    return render(request, 'change_password.html', context)


def ForgetPassword(request):
    try:
        users = User.objects.all()
        print(users)
        if request.method == 'POST':
            somedata = request.POST.get('inputsomething')

            if User.objects.filter(username=somedata).first():
                user_obj = User.objects.get(username=somedata)
                profile = Profile.objects.filter(user=user_obj).first()
                auth_token = profile.auth_token
                print(profile)

                send_mail_for_password_reset(
                    email=user_obj.email, auth_token=auth_token, fname=user_obj.first_name)
                messages.success(
                    request, 'An email is sent to your registered email.')
                return redirect('forget_password')
            elif User.objects.filter(email=somedata).first():
                user_obj = User.objects.get(email=somedata)
                profile = Profile.objects.filter(user=user_obj).first()
                auth_token = profile.auth_token
                print(profile)

                send_mail_for_password_reset(
                    email=user_obj.email, auth_token=auth_token, fname=user_obj.first_name)
                messages.success(
                    request, 'An email is sent to your registered email.')
                return redirect('forget_password')
            else:
                messages.success(request, 'No user found.')
                return redirect('forget_password')

    except Exception as e:
        print(e)
    return render(request, 'forgot_password.html')


def send_mail_for_password_reset(email, auth_token, fname):
    subject = 'Your account need to be verified'
    link = f'https://311alert.info/password-reset-verification/{auth_token}'

    context = {
        "link": link,
        "fname": fname,
    }

    from_email = settings.EMAIL_HOST_USER

    templ = get_template('resettempletext.txt')
    messageing = templ.render(context)
    emailnew = EmailMultiAlternatives(
        subject, messageing, from_email,  [email])

    emailnew.content_subtype = 'html'
    emailnew.send()


def send_mail_after_registration(email, auth_token, fname):
    subject = 'Your account needs to be verified'
    link = auth_token

    context = {
        "link": link,
        "fname": fname,
    }

    from_email = settings.EMAIL_HOST_USER

    templ = get_template('templetext.txt')
    messageing = templ.render(context)
    emailnew = EmailMultiAlternatives(
        subject, messageing, from_email, [email])

    emailnew.content_subtype = 'html'
    print(context)
    print(subject)
    emailnew.send()
    print(emailnew)


def logout_attempt(request):
    logout(request)
    return redirect('/')


def verified_email(user):
    subject = 'Welcome to 311Alert'
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
        subject, messageing, from_email, [user.email])

    emailnew.content_subtype = 'html'
    emailnew.send()
