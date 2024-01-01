
from django.contrib.auth.decorators import login_required
from .models import Property, HPDComplaints, HPDViolations, HPDCharges, HPDLitigation, HPDRepair, HPDBedBugReport
from django.db.models import Count, Q
from django.shortcuts import render


def hpd_data(request):
    return render(request, 'hpd.html')


@login_required
def hpd_complaints(request):
    user_properties = Property.objects.filter(
        hpd_complaints__isnull=False, user=request.user).distinct()

    properties = user_properties.annotate(
        num_open_complaints=Count('hpd_complaints', filter=Q(
            hpd_complaints__complaint_status__icontains='open')),
        num_total_complaints=Count('hpd_complaints'),
    )

    context = {

        "properties": properties
    }
    return render(request, 'hpd_complaints.html', context)


@login_required
def hpd_complaints_by_property(request, id):

    property = Property.objects.get(id=id)

    complaints = HPDComplaints.objects.filter(property=property).order_by('complaint_status')
    context = {

        "complaints": complaints,
        "property": property
    }
    return render(request, 'hpd_complaints_by_property.html', context)


@login_required
def hpd_violations(request):

    # Get all properties with at least one complaint.
    properties = Property.objects.filter(
        hpd_violations__isnull=False, user=request.user).distinct()

    properties = properties.annotate(
        num_open_violations=Count('hpd_violations', filter=Q(
            hpd_violations__violationstatus__icontains='open')),
        num_total_violations=Count('hpd_violations'),
    )

    context = {

        "properties": properties
    }
    return render(request, 'hpd_violations.html', context)


@login_required
def hpd_violations_by_property(request, id):

    property = Property.objects.get(id=id)

    violations = HPDViolations.objects.filter(property=property).order_by('violationstatus')
    context = {

        "violations": violations,
        "property": property
    }
    return render(request, 'hpd_violations_by_property.html', context)


@login_required
def hpd_charges(request):

    # Get all properties with at least one complaint.
    properties = Property.objects.filter(
        hpd_charges__isnull=False, user=request.user).distinct()

    context = {

        "properties": properties
    }
    return render(request, 'hpd_charges.html', context)


@login_required
def hpd_charges_by_property(request, id):

    property = Property.objects.get(id=id)

    charges = HPDCharges.objects.filter(property=property)
    context = {

        "charges": charges,
        "property": property
    }
    return render(request, 'hpd_charges_by_property.html', context)


@login_required
def hpd_ligitations(request):

    # Get all properties with at least one complaint.
    properties = Property.objects.filter(
        hpd_litigations__isnull=False, user=request.user).distinct()

    context = {

        "properties": properties
    }
    return render(request, 'hpd_litigations.html', context)


@login_required
def hpd_ligitations_by_property(request, id):

    property = Property.objects.get(id=id)

    litigations = HPDLitigation.objects.filter(property=property)
    context = {

        "litigations": litigations,
        "property": property
    }
    return render(request, 'hpd_litigations_by_property.html', context)


@login_required
def hpd_repais_orders(request):

    # Get all properties with at least one complaint.
    properties = Property.objects.filter(
        hpd_repairs__isnull=False, user=request.user).distinct()

    context = {

        "properties": properties
    }
    return render(request, 'hpd_repair.html', context)


@login_required
def hpd_repais_orders_by_property(request, id):

    property = Property.objects.get(id=id)

    hpd_repairs = HPDRepair.objects.filter(property=property)
    context = {

        "hpd_repairs": hpd_repairs,
        "property": property
    }
    return render(request, 'hpd_repair_by_property.html', context)


@login_required
def hpd_bedbug(request):

    # Get all properties with at least one complaint.
    properties = Property.objects.filter(
        hpd_bedbugs__isnull=False, user=request.user).distinct()

    context = {

        "properties": properties
    }
    return render(request, 'hpd_bedbugs.html', context)


@login_required
def hpd_bedbug_by_property(request, id):

    property = Property.objects.get(id=id)

    bedbugs = HPDBedBugReport.objects.filter(property=property)
    context = {

        "bedbugs": bedbugs,
        "property": property
    }
    return render(request, 'hpd_bedbugs_by_property.html', context)
