
from django.contrib.auth.decorators import login_required
from .models import Complaints, Voilation, HPDComplaints
from django.db.models import Count, Q
from django.shortcuts import render
from .models import Property


def dob_data(request):
    return render(request, 'dob.html')


@login_required
def complaints(request):

    properties = Property.objects.filter(
        complaints__isnull=False, user=request.user).distinct()

    context = {

        "properties": properties
    }
    return render(request, 'complaints.html', context)


@login_required
def complaints_by_property(request, id):

    property = Property.objects.get(id=id)

    complaints = Complaints.objects.filter(property=property).order_by('status')
    context = {

        "complaints": complaints,
        "property": property
    }
    return render(request, 'complaints_by_property.html', context)


@login_required
def violations(request):
    properties = Property.objects.filter(
        voilations__isnull=False, user=request.user).distinct()

    context = {

        "properties": properties
    }
    return render(request, 'violations.html', context)


@login_required
def violations_by_property(request, id):
    property = Property.objects.get(id=id)

    violations = Voilation.objects.filter(
        property=property).order_by('-violation_category')

    context = {
        "property": property,
        "violations": violations,

    }
    return render(request, 'violations_by_property.html', context)
