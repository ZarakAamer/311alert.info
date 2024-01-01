from django.shortcuts import render, redirect
from django.db.models import Min
from django.db.models import Subquery
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Profile, Property, AdditionalContact
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from twilio.rest import Client


account_sid = settings.ACC_SID
auth_token = settings.AUTH_TOKEN
phone_number = settings.PHONE_NUMBER


def property_notifications(context, subject, request, template_name, heading):
    from_email = settings.EMAIL_HOST_USER

    templ = get_template(f'{template_name}.txt')
    messageing = templ.render(context)
    emailnew = EmailMultiAlternatives(
        subject, messageing, from_email, [request.user.email])

    emailnew.content_subtype = 'html'
    emailnew.send()
    try:
        client = Client(account_sid, auth_token)

        if context["property_name"] == '':
            message = client.messages.create(
                body=f'''{heading}
                    \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
                    \n \n {context["block"]} \n \n {context["lott"]}
                    \n \n {context["bin_number"]} \n \n support@311alert.info
                ''',
                from_=phone_number,
                to=request.user.phone
            )
        else:
            message = client.messages.create(
                body=f'''{heading}
                    \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
                    \n \n {context["block"]} \n \n {context["lott"]}
                    \n \n {context["bin_number"]} \n \n {context["property_name"]} \n \n support@311alert.info
                ''',
                from_=phone_number,
                to=request.user.phone
            )

        print(message.sid)
    except Exception as e:
        print(e)


def add_property(request):
    if request.method == "POST":
        property_name = request.POST.get('property_name')
        zip = request.POST.get('zip')
        borough = request.POST.get('borough')
        block = request.POST.get('block')
        lott = request.POST.get('lott')
        street = request.POST.get('street')
        house = request.POST.get('house')
        bin_number = request.POST.get('bin_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name1 = request.POST.get('name1')
        email1 = request.POST.get('email1')
        phone1 = request.POST.get('phone1')
        name2 = request.POST.get('name2')
        email2 = request.POST.get('email2')
        phone2 = request.POST.get('phone2')
        additional = request.POST.get('additional')
        additional1 = request.POST.get('additional1')
        additional2 = request.POST.get('additional2')

        property = Property(user=request.user, property_name=property_name, zip=zip, borough=borough,
                            block=block, lott=lott, street=street, house=house, bin_number=bin_number,)
        property.save()

        if additional == 'already':
            if name == "" and email == "" and phone == "":
                pass
            else:
                AdditionalContact(user=request.user, property=property,
                                  name=name, email=email, phone=phone).save()
        else:
            id = additional.split(",")[0]
            print(id)
            contact_ = AdditionalContact.objects.get(id=id)
            if contact_:
                AdditionalContact(user=request.user, property=property,
                                  name=contact_.name, email=contact_.email, phone=contact_.phone).save()
            else:
                pass

        if additional1 == 'already':

            if name1 == "" and email1 == "" and phone1 == "":
                pass
            else:
                AdditionalContact(user=request.user, property=property,
                                  name=name1, email=email1, phone=phone1).save()
        else:
            contact__ = AdditionalContact.objects.get(id=additional1)
            if contact__:
                AdditionalContact(user=request.user, property=property,
                                  name=contact__.name, email=contact__.email, phone=contact__.phone).save()
            else:
                pass

        if additional2 == 'already':

            if name2 == "" and email2 == "" and phone2 == "":
                pass
            else:
                AdditionalContact(user=request.user, property=property,
                                  name=name2, email=email2, phone=phone2).save()
        else:
            contact___ = AdditionalContact.objects.get(id=additional2)
            if contact___:
                AdditionalContact(user=request.user, property=property,
                                  name=contact___.name, email=contact___.email, phone=contact___.phone).save()
            else:
                pass

        subject = 'Property was added'
        context = {
            "status": "Property with the following details Added successfully.",
            "borough": f'Borough:  {borough}',
            "property_name": f'Property Name:  {property_name}',
            "zip": zip,
            "block": f'Block:  {block}',
            "lott": f'Lot:  {lott}',
            "house": f'House:  {house}',
            "street": f'Street:  {street}',
            "bin_number": f'BIN #:  #{bin_number}',
            "fname": request.user.first_name,
        }
        template_name = 'property_add_delete'
        heading = 'Property was Added'
        property_notifications(context, subject, request,
                               template_name, heading)

        # from_email = settings.EMAIL_HOST_USER

        # templ = get_template('property_add_delete.txt')
        # messageing = templ.render(context)
        # emailnew = EmailMultiAlternatives(
        #     subject, messageing, from_email, [request.user.email])

        # emailnew.content_subtype = 'html'
        # emailnew.send()
        # try:
        #     client = Client(account_sid, auth_token)

        #     if context["property_name"] == '':
        #         message = client.messages.create(
        #             body=f'''Property was Added
        #                 \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
        #                 \n \n {context["block"]} \n \n {context["lott"]}
        #                 \n \n {context["bin_number"]}  \n \n support@311alert.info
        #             ''',
        #             from_=phone_number,
        #             to=request.user.phone
        #         )
        #         print(message)

        #     else:
        #         message = client.messages.create(
        #             body=f'''Property was Added
        #                 \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
        #                 \n \n {context["block"]} \n \n {context["lott"]}
        #                 \n \n {context["bin_number"]} \n \n {context["property_name"]} \n \n support@311alert.info
        #             ''',
        #             from_=phone_number,
        #             to=request.user.phone
        #         )
        #         print(message)
        # except Exception as e:
        #     print(e)

    return redirect('add_property')


def edit_property_page(request, property_id):
    pro = Property.objects.get(id=property_id)
    contacts = AdditionalContact.objects.filter(property=pro)

    return render(request, 'edit_property.html', {"pro": pro, "contacts": contacts})


def edit_contact(request, contact_id):
    contact = AdditionalContact.objects.get(id=contact_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        property_id = request.POST.get('property_id')

        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.save()

    return redirect(f'/edit-property-page/{property_id}')


def edit_property(request, property_id):
    if request.method == "POST":
        property_name = request.POST.get('property_name')
        zip = request.POST.get('zip')
        borough = request.POST.get('borough')
        block = request.POST.get('block')
        lott = request.POST.get('lott')
        street = request.POST.get('street')
        house = request.POST.get('house')
        bin_number = request.POST.get('bin_number')

        property = Property.objects.get(id=property_id)
        property.property_name = property_name
        property.zip = zip
        property.borough = borough
        property.block = block
        property.lott = lott
        property.street = street
        property.house = house
        property.bin_number = bin_number

        property.save()
        subject = 'Property was Edited'
        context = {
            "status": "Property with the following details Edited successfully.",
            "borough": f'Borough: {borough}',
            "property_name": f'Property Name: {property_name}',
            "zip": zip,
            "block": f'Block: {block}',
            "lott": f'Lot: {lott}',
            "house": f'House: {house}',
            "street": f'Street: {street}',
            "bin_number": f'BIN#: {bin_number}',
            "fname": request.user.first_name,
        }

        template_name = 'property_add_delete'
        heading = 'Property was Edited'
        property_notifications(context, subject, request,
                               template_name, heading)

        # from_email = settings.EMAIL_HOST_USER

        # templ = get_template('property_add_delete.txt')
        # messageing = templ.render(context)
        # emailnew = EmailMultiAlternatives(
        #     subject, messageing, from_email, [request.user.email])

        # emailnew.content_subtype = 'html'
        # emailnew.send()
        # try:
        #     client = Client(account_sid, auth_token)

        #     if context["property_name"] == '':
        #         message = client.messages.create(
        #             body=f'''Property was Edited
        #                 \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
        #                 \n \n {context["block"]} \n \n {context["lott"]}
        #                 \n \n {context["bin_number"]} \n \n support@311alert.info
        #             ''',
        #             from_=phone_number,
        #             to=request.user.phone
        #         )
        #     else:
        #         message = client.messages.create(
        #             body=f'''Property was Edited
        #                 \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
        #                 \n \n {context["block"]} \n \n {context["lott"]}
        #                 \n \n {context["bin_number"]} \n \n {context["property_name"]} \n \n support@311alert.info
        #             ''',
        #             from_=phone_number,
        #             to=request.user.phone
        #         )

        #     print(message.sid)
        # except Exception as e:
        #     print(e)

    return redirect(f'/edit-property-page/{property_id}')


@login_required
def add_properties(request):
    if request.user.is_authenticated:
        # try:
        profile = Profile.objects.filter(
            user=request.user, is_pro=True).first()
        if profile:
            all_properties = Property.objects.filter(
                user=request.user)

            distinct_contacts = AdditionalContact.objects.filter(user=request.user).values(
                'name', 'email'
            ).annotate(
                min_id=Min('id')
            )

            # Retrieve the corresponding unique instances
            contact_list = AdditionalContact.objects.filter(id__in=Subquery(
                distinct_contacts.values('min_id')
            ))

            # contacts = AdditionalContact.objects.filter(user=request.user)
            # for i in contacts:
            #     if i not in contact_list:
            #         contact_list.append(i)
            #     else:
            #         pass

            length = len(all_properties)
            if length < profile.can_add:

                context = {
                    "profile": profile,
                    "contact_list": contact_list
                }
                # messages.success(request, "Property Added!")

                return render(request, 'add-property.html', context)

            else:
                messages.warning(request, "You have reached the limit!")
                context = {"limit_reached": True,
                           "properties": Property.objects.filter(user=request.user)}
                return render(request, "property.html", context)

        else:
            messages.warning(request, "You have to buy a package!")

            return redirect('price')
    else:
        return redirect('login')


def delete_street_property(request, pro_id):
    if Property.objects.get(id=pro_id):
        property = Property.objects.get(id=pro_id)
        subject = 'Property was Deleted'
        context = {
            "status": "Property with the following details was deleted.",
            "borough": f'Borough: {property.borough} ',
            "property_name": f'Property Name: {property.property_name} ',

            "zip": property.zip,
            "block": f'Block: {property.block} ',
            "lott": f'Lot: {property.lott} ',
            "house": f'House: {property.house} ',
            "street": f'Street: {property.street} ',
            "bin_number": f'BIN#: {property.bin_number} ',
            "fname": request.user.first_name,
        }

        template_name = 'property_add_delete'
        heading = 'Property was Deleted'
        property_notifications(context, subject, request,
                               template_name, heading)

        # from_email = settings.EMAIL_HOST_USER

        # templ = get_template('property_add_delete.txt')
        # messageing = templ.render(context)
        # emailnew = EmailMultiAlternatives(
        #     subject, messageing, from_email, [request.user.email])

        # emailnew.content_subtype = 'html'
        # emailnew.send()
        # try:
        #     client = Client(account_sid, auth_token)
        #     if context["property_name"] == '':
        #         message = client.messages.create(
        #             body=f'''Property was Deleted
        #                 \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
        #                 \n \n {context["block"]} \n \n {context["lott"]}
        #                 \n \n {context["bin_number"]} \n \n  support@311alert.info
        #             ''',
        #             from_=phone_number,
        #             to=request.user.phone
        #         )
        #     else:
        #         message = client.messages.create(
        #             body=f'''Property was Deleted
        #                 \n \n {context["borough"]} \n \n {context["house"]} \n \n {context["street"]}
        #                 \n \n {context["block"]} \n \n {context["lott"]}
        #                 \n \n {context["bin_number"]} \n \n {context["property_name"]} \n \n support@311alert.info
        #             ''',
        #             from_=phone_number,
        #             to=request.user.phone
        #         )

        #     print(message.sid)
        # except Exception as e:
        #     print(e)
        # print(context)

        property.delete()

        return redirect('properties_page')
    return redirect('properties_page')
