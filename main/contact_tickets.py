from captcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField
from django import forms
from django.shortcuts import render, redirect
import datetime
import time
from django.db.models import Min
from django.db.models import Subquery, OuterRef

import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Profile, Property, Price, Contact, AdditionalContact
from .models import Privacy, Terms
import stripe
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User, UserCredsSaver, Userpayments
import uuid
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.http import HttpResponse
import os
from twilio.rest import Client
from .models import Complaints, Voilation
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket, TicketReply
import random


@login_required
def tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    context = {
        "tickets": tickets
    }
    return render(request, 'tickets.html', context)


@login_required
def ticket_details(request, id):
    ticket = Ticket.objects.get(id=id)
    context = {
        "ticket": ticket
    }
    return render(request, 'ticket-details.html', context)


@login_required
def reply_ticket(request):

    if request.method == 'POST':
        reply = request.POST.get("reply")
        id = request.POST.get("ticket")

        ticket = Ticket.objects.get(id=id)

        TicketReply.objects.create(
            user=request.user, ticket=ticket, description=reply)

        email = EmailMessage(
            subject=f"Rreply for ticket {id}",
            body=reply,
            from_email=settings.EMAIL1_HOST_USER,
            to=[settings.EMAIL1_HOST_USER, ]
        )
        email.send()
    return redirect('/')




def ticket_ressolved(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.is_ressolved = True
    ticket.save()
    return redirect('/')


@login_required
def ticket(request):
    if request.user.is_authenticated:
        return render(request, 'ticket.html')
    else:
        return redirect('/')


@login_required
def ticket_process(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        tick = Ticket.objects.create(
            user=request.user, subject=subject, description=description)
        subject = 'Ticket Created! '

        context = {
            "id": tick.id,
            "fname": request.user.first_name,
        }

        from_email = settings.EMAIL1_HOST_USER

        templ = get_template('tickettemplate.txt')
        messageing = templ.render(context)
        emailnew = EmailMultiAlternatives(
            subject, messageing, from_email, [request.user.email])

        emailnew.content_subtype = 'html'
        emailnew.send()

        email = EmailMessage(
            subject=f"ticket id {tick.id}",
            body=description,
            from_email=settings.EMAIL1_HOST_USER,
            to=[settings.EMAIL1_HOST_USER, ]
        )
        email.send()

    return redirect('home')


def contact(request):
    return render(request, 'contact.html')


def contact_process(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email,
                               subject=subject, message=message)

    return redirect('home')
