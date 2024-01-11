
from django.shortcuts import render, redirect
from .models import Privacy, Terms, Profile, Price, Upload
from django.contrib import messages


def handler404(request, exception):
    return render(request, '404.html', status=404)


def home(request):

    try:
        if request.user.is_authenticated:
            profile_object = Profile.objects.filter(user=request.user).first()
            if profile_object.is_pro:
                return render(request, 'profile_page.html')
            else:
                prices = Price.objects.all()
                return render(request, 'index.html', {"prices": prices})
        else:
            prices = Price.objects.all()
            return render(request, 'index.html', {"prices": prices})

    except Exception as e:
        print(e)
        messages.error(
            request, f"{e} {request.user.email}")
        prices = Price.objects.all()
        return render(request, 'index.html', {"prices": prices})


def pro_home(request):
    try:

        if request.user.is_authenticated:
            profile_object = Profile.objects.filter(user=request.user).first()
            if profile_object.is_pro:
                prices = Price.objects.all()
                return render(request, 'index.html', {"profiled": True, "prices": prices})
            else:
                return redirect("home")
        else:
            return redirect("home")

    except Exception as e:
        print(e)
        messages.error(
            request, f" {e} {request.user.email}")
        prices = Price.objects.all()
        return render(request, 'index.html', {"prices": prices})


def princing(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile.is_pro == True:
            prices = Price.objects.all()
            context = {"profiled": profile,
                       "prices": prices}
            return render(request, 'pricing.html', context)
        else:
            prices = Price.objects.all()
            return render(request, 'pricing.html', {"prices": prices})
    else:
        prices = Price.objects.all()
        return render(request, 'pricing.html', {"prices": prices})


def privacy_policy(request):
    privacy = Privacy.objects.all()[0]
    return render(request, 'privacy_policy.html', {"privacy": privacy})


def terms_of_use(request):
    terms = Terms.objects.all()[0]
    return render(request, 'terms_of_use.html', {"terms": terms})


def about_us(request):
    return render(request, 'about.html')


def upload(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        Upload.objects.create(file=file)
    return redirect("home")


def uploading(request):
    return render(request, "uploading.html")
