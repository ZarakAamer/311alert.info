
from .models import *
from django.shortcuts import render


def properties_page(request):
    properties = Property.objects.filter(user=request.user)

    return render(request, 'property.html', {"properties": properties})


def property_details_page(request, property_id):
    pro = Property.objects.get(id=property_id)
    complaints = Complaints.objects.filter(property=pro)
    violations = Voilation.objects.filter(property=pro)
    hpd_complaints = HPDComplaints.objects.filter(property=pro)
    hpd_violations = HPDViolations.objects.filter(property=pro)
    hpd_charges = HPDCharges.objects.filter(property=pro)
    hpd_litigations = HPDLitigation.objects.filter(property=pro)
    hpd_repairs = HPDRepair.objects.filter(property=pro)
    hpd_bedbugs = HPDBedBugReport.objects.filter(property=pro)

    contacts = pro.contacts.all()
    context = {
        "pro": pro,
        "complaints": complaints,
        "violations": violations,
        "hpd_complaints": hpd_complaints,
        "hpd_violations": hpd_violations,
        "hpd_charges": hpd_charges,
        "hpd_litigations": hpd_litigations,
        "hpd_repairs": hpd_repairs,
        "hpd_bedbugs": hpd_bedbugs,
        "contacts": contacts,
    }

    return render(request, 'detail_property.html', context)


def property_search_page(request):

    return render(request, 'search_property.html')
