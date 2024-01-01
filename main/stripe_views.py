from django.contrib.auth.decorators import login_required
from .models import User,  Userpayments, Profile, Price
from django.views.decorators.csrf import csrf_exempt
from captcha.widgets import ReCaptchaV2Checkbox
from django.shortcuts import render, redirect
from captcha.fields import ReCaptchaField
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.conf import settings
from django import forms
import stripe
import time


stripe.api_key = settings.STRIPE_KEY
stripe_public_keys = settings.STRIPE_PUBLIC_KEY
end_point_secret = settings.WEBHOOK_KEY


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'label': ''}))


def payment_after_registeration(request, param1):
    user = User.objects.get(id=param1)
    price = Price.objects.all()
    print(f"Hello this is the id at payment after registration View {user.id}")
    context = {
        "captcha": FormWithCaptcha,

        "user_id": user.id,
        "prices": price,
        "stripekeypublick": stripe_public_keys
    }

    return render(request, 'choose_package.html', context)


def payment_at_registration(request):
    now = datetime.now()
    thirty_days_from_now = now + timedelta(days=30)
    if request.method == 'POST':
        form = FormWithCaptcha(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)

            account_type = request.POST.get('account_type')

            if Price.objects.filter(first_month_token=account_type).exists():
                price_from_model = Price.objects.filter(
                    first_month_token=account_type).first()

                next_price_id = price_from_model.subsequent_months_token

                try:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=user.first_name+" "+user.last_name,
                        source=request.POST['stripeToken']
                    ).save()
                    print("Customer was created")
                    print(customer)


                    subscription = stripe.Subscription.create(
                        customer=customer["id"],
                        items=[{'price': next_price_id}],
                        trial_end=thirty_days_from_now

                    )

                    print("Subscription was created")
                    print(subscription)

                    profile.is_pro = True
                    profile.can_add = 1
                    profile.strip_subscription_token = subscription["id"]
                    profile.strip_costumer_token = customer["id"]
                    profile.pro_start_date = datetime.now()
                    profile.is_yearly = False
                    profile.save()

                    Userpayments.objects.create(
                        user=user, payment=10, payment_is_yearly=False, customer_token=customer["id"], subscription_token=subscription["id"])
                    return render(request, 'success.html')

                except stripe.error.CardError as e:
                    return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))

                except stripe.error.RateLimitError as e:
                    # handle this e, which could be stripe related, or more generic
                    return HttpResponse("<h1>Rate error!</h1>")

                except stripe.error.InvalidRequestError as e:
                    return HttpResponse("<h1>Invalid request error!</h1>")

                except stripe.error.AuthenticationError as e:
                    return HttpResponse("<h1>Invalid Auth Error!</h1>")

                except stripe.error.StripeError as e:
                    return HttpResponse("<h1>Invalid error!</h1>")

                except Exception as e:
                    return render(request, 'cancel.html')

            elif Price.objects.filter(first_year_token=account_type).exists():
                price_from_model = Price.objects.filter(
                    first_year_token=account_type).first()
                yearly_token = price_from_model.first_year_token

                try:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=user.first_name+" "+user.last_name,
                        source=request.POST['stripeToken']
                    )

                    customer.save()

                    subscription = stripe.Subscription.create(
                        customer=customer["id"],
                        items=[{'price': yearly_token}],
                    )

                    profile.is_pro = True
                    profile.can_add = 1
                    profile.strip_subscription_token = subscription["id"]
                    profile.strip_costumer_token = customer["id"]
                    profile.pro_start_date = datetime.now()
                    profile.is_yearly = True
                    profile.save()

                    Userpayments.objects.create(
                        user=user, payment=36, payment_is_yearly=True, customer_token=customer["id"], subscription_token=subscription["id"])
                    return render(request, 'success.html')

                except stripe.error.CardError as e:
                    return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))

                except stripe.error.RateLimitError as e:
                    # handle this e, which could be stripe related, or more generic
                    return HttpResponse("<h1>Rate error!</h1>")

                except stripe.error.InvalidRequestError as e:
                    return HttpResponse("<h1>Invalid request error!</h1>")

                except stripe.error.AuthenticationError as e:
                    return HttpResponse("<h1>Invalid Auth Error!</h1>")

                except stripe.error.StripeError as e:
                    return HttpResponse("<h1>Invalid error!</h1>")

                except Exception as e:
                    return render(request, 'cancel.html')

        else:
            print('Form errors:', form.errors)
            context = {
                "captcha": form,
                "user_id": request.POST.get('user_id'),
                "prices": Price.objects.all()
            }
            return render(request, 'choose_package.html', context)
    else:
        return redirect('price')


def success_third(request):

    return render(request, 'success.html')


# @login_required(login_url='login')
def become_pro(request):
    now = datetime.now()
    thirty_days_from_now = now + timedelta(days=30)
    if request.user.is_authenticated:
        if request.method == 'POST':

            user_id = request.user.id
            account_type = request.POST.get('account_type')
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)
            if Price.objects.filter(first_month_token=account_type).exists():
                price_from_model = Price.objects.filter(
                    first_month_token=account_type).first()

                next_price_id = price_from_model.subsequent_months_token

                try:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=user.first_name+" "+user.last_name,
                        source=request.POST['stripeToken']
                    ).save()
                    print("Customer was created")
                    print(customer)

                
                    subscription = stripe.Subscription.create(
                        customer=customer["id"],
                        items=[{'price': next_price_id}],
                        trial_end=thirty_days_from_now

                    )

                    print("Subscription was created")
                    print(subscription)

                    profile.is_pro = True
                    profile.can_add = 1
                    profile.strip_subscription_token = subscription["id"]
                    profile.strip_costumer_token = customer["id"]
                    profile.pro_start_date = datetime.now()
                    profile.is_yearly = False
                    profile.save()

                    Userpayments.objects.create(
                        user=user, payment=10, payment_is_yearly=False, customer_token=customer["id"], subscription_token=subscription["id"])
                    return render(request, 'success.html')

                except stripe.error.CardError as e:
                    return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))

                except stripe.error.RateLimitError as e:
                    # handle this e, which could be stripe related, or more generic
                    return HttpResponse("<h1>Rate error!</h1>")

                except stripe.error.InvalidRequestError as e:
                    return HttpResponse("<h1>Invalid request error!</h1>")

                except stripe.error.AuthenticationError as e:
                    return HttpResponse("<h1>Invalid Auth Error!</h1>")

                except stripe.error.StripeError as e:
                    return HttpResponse("<h1>Invalid error!</h1>")

                except Exception as e:
                    return render(request, 'cancel.html')

            elif Price.objects.filter(first_year_token=account_type).exists():
                price_from_model = Price.objects.filter(
                    first_year_token=account_type).first()
                yearly_token = price_from_model.subsequent_years_token
                price_first_month_id = price_from_model.first_year_token

                try:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=user.first_name+" "+user.last_name,
                        source=request.POST['stripeToken']
                    )

                    customer.save()

                    subscription = stripe.Subscription.create(
                        customer=customer["id"],
                        items=[{'price': yearly_token}],
                    )

                    profile.is_pro = True
                    profile.can_add = 1
                    profile.strip_subscription_token = subscription["id"]
                    profile.strip_costumer_token = customer["id"]
                    profile.pro_start_date = datetime.now()
                    profile.is_yearly = True
                    profile.save()

                    Userpayments.objects.create(
                        user=user, payment=36, payment_is_yearly=True, customer_token=customer["id"], subscription_token=subscription["id"])
                    return render(request, 'success.html')

                except stripe.error.CardError as e:
                    return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))

                except stripe.error.RateLimitError as e:
                    # handle this e, which could be stripe related, or more generic
                    return HttpResponse("<h1>Rate error!</h1>")

                except stripe.error.InvalidRequestError as e:
                    return HttpResponse("<h1>Invalid request error!</h1>")

                except stripe.error.AuthenticationError as e:
                    return HttpResponse("<h1>Invalid Auth Error!</h1>")

                except stripe.error.StripeError as e:
                    return HttpResponse("<h1>Invalid error!</h1>")

                except Exception as e:
                    return render(request, 'cancel.html')

        return redirect('price')
    else:
        return redirect("register")


def calculate_prorated_amount(profile, subscription, updated_subscription, number_of_properties):
    import datetime
    """Calculates the prorated amount for a subscription change.

    Args:
      subscription: The current subscription.
      updated_subscription: The updated subscription.
      number_of_properties: The number of properties.

    Returns:
      The prorated amount.
    """

    new_price = number_of_properties * \
        int(updated_subscription['plan']['amount']) / 100

    current_billing_period_start = datetime.datetime.fromtimestamp(
        subscription['current_period_start'])
    print(f"current_billing_period_start {current_billing_period_start}")

    current_billing_period_end = datetime.datetime.fromtimestamp(
        subscription['current_period_end'])
    print(f"current_billing_period_End {current_billing_period_end}")

    number_of_days_in_billing_period = (
        current_billing_period_end - current_billing_period_start).days
    print(
        f"number_of_days_in_billing_period {number_of_days_in_billing_period}")

    cost_of_subscription_for_current_billing_period = int(
        subscription['plan']['amount']) / 100 * int(profile.can_add)
    print(
        f"cost_of_subscription_for_current_billing_period {cost_of_subscription_for_current_billing_period}")

    cost_of_subscription_for_new_billing_period = new_price
    print(
        f"cost_of_subscription_for_new_billing_period {cost_of_subscription_for_new_billing_period}")

    today = datetime.datetime.now()
    remaining_days = (current_billing_period_end - today).days
    print(f"remaining_days {remaining_days}")

    daily_rate = cost_of_subscription_for_current_billing_period / \
        number_of_days_in_billing_period
    print(f"daily_rate {daily_rate}")

    print(f"Profile_can_add {profile.can_add}")
    proration_amount = daily_rate * remaining_days

    return proration_amount


@login_required
def change_subscription(request):
    if request.method == 'POST':
        user_obj = request.user
        profile = Profile.objects.filter(user=user_obj).first()
        number_of_properties = int(
            request.POST.get('number')) + int(profile.can_add)
        new_billing_interval = request.POST.get('subscription_interval')

        price = Price.objects.first()

        is_yearly = None
        if new_billing_interval == price.price_change_to_month:
            is_yearly = False
        elif new_billing_interval == price.price_change_to_year:
            is_yearly = True

        try:
            customer = stripe.Customer.retrieve(profile.strip_costumer_token)
            subscription = stripe.Subscription.retrieve(
                profile.strip_subscription_token)
            
            subscription_id = subscription['items']['data'][0]['id']
            if subscription.trial_end:
                updated_subscription = stripe.Subscription.modify(
                    subscription.id,
                    proration_behavior='create_prorations',
                    items=[{
                        # 'id': subscription['items']['data'][0].id,
                        'id': subscription_id,
                        'price': new_billing_interval,
                        'quantity': number_of_properties,
                    }],
                    metadata={
                        "updated": "yes",
                        "user_id": user_obj.id,
                        'next_price_id': new_billing_interval,
                        "properties": number_of_properties,
                    },
                    trial_end="now",
                    proration_date=int(time.time()),
                    # Start the new billing cycle immediately
                    billing_cycle_anchor="now",
                )
            else:
                updated_subscription = stripe.Subscription.modify(
                    subscription.id,
                    proration_behavior='create_prorations',
                    items=[{
                        # 'id': subscription['items']['data'][0].id,
                        'id': subscription_id,
                        'price': new_billing_interval,
                        'quantity': number_of_properties,
                    }],
                    metadata={
                        "updated": "yes",
                        "user_id": user_obj.id,
                        'next_price_id': new_billing_interval,
                        "properties": number_of_properties,
                    },
                    proration_date=int(time.time()),
                    # Start the new billing cycle immediately
                    billing_cycle_anchor="now",
                )
            proration_amount = calculate_prorated_amount(profile,
                                                         subscription, updated_subscription, number_of_properties)

            print("This is the proration amount hehehe")
            print(proration_amount)
            profile.can_add = number_of_properties

            profile.strip_subscription_token = updated_subscription["id"]

            profile.is_yearly = is_yearly

            profile.save()
            Userpayments.objects.create(
                user=profile.user, payment=proration_amount, payment_is_yearly=profile.is_yearly, customer_token=profile.strip_costumer_token, subscription_token=updated_subscription["id"])

            return redirect('success_2')

        except stripe.error.CardError as e:
            return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))

        except stripe.error.RateLimitError as e:
            # handle this e, which could be stripe related, or more generic
            return HttpResponse("<h1>Rate error!</h1>")

        except stripe.error.InvalidRequestError as e:
            return HttpResponse(f"<h1>Invalid request error! </h1> <p>{e}</p>")

        except stripe.error.AuthenticationError as e:
            return HttpResponse("<h1>Invalid Auth Error!</h1>")

        except stripe.error.StripeError as e:
            return HttpResponse(f"<h1>Invalid error!</h1> <p>{e}</p>")

        except Exception as e:
            return render(request, 'cancel.html', {"e": e})

    return render(request, 'update_subscrption.html')


def update_subscription(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    price = Price.objects.all()[0]
    return render(request, 'update_subscrption.html', {"price": price, "profile": profile})


def already_pro(request):
    return render(request, 'pro_user.html')


def success_second(request):
    return render(request, 'success2.html')


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


def twenty_plus(request):
    return render(request, 'twenty_plus.html')





@login_required
def my_subscriptions(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    subscription = subscription = stripe.Subscription.retrieve(
        profile.strip_subscription_token)
    # print(subscription)

    # price = subscription["plan"]["amount"] / 100
    created_at = subscription["created"]
    current_period_start = subscription["current_period_start"]
    current_period_end = subscription["current_period_end"]
    # plan_name = subscription["plan"]

    created_at_date = datetime.fromtimestamp(created_at)
    current_period_start_date = datetime.fromtimestamp(
        current_period_start)
    current_period_end_date = datetime.fromtimestamp(
        current_period_end)

    today = datetime.today()

    delta = current_period_end_date - today

    created_at_date = datetime.fromtimestamp(
        created_at).strftime('%m/%d/%Y')
    current_period_start_date = datetime.fromtimestamp(
        current_period_start).strftime('%m/%d/%Y')
    current_period_end_date = datetime.fromtimestamp(
        current_period_end).strftime('%m/%d/%Y')

    number_of_days = delta.days

    calculate_life = int(number_of_days)/30 * 100
    life = 100-calculate_life

    # cards = stripe.Customer.list_sources(
    #     profile.strip_costumer_token,
    #     object='card',
    # )
    # print(cards)
    custom = stripe.Customer.retrieve(profile.strip_costumer_token)

    payment_methods = stripe.PaymentMethod.list(
        customer=custom,
        type='card'  # You can specify the type if you are interested in card payment methods
    )
    # print(custom.id)
    for payment_method in payment_methods:
        card = payment_method.card
        last4 = card.last4
        brand = card.brand
        exp_month = card.exp_month
        exp_year = card.exp_year

        # print(f"Last 4 digits: {last4}")
        # print(f"Brand: {brand}")
        # print(f"Expiration Date: {exp_month}/{exp_year}")
        # print()

    custom = stripe.Customer.retrieve(profile.strip_costumer_token)

    default_payment_method = custom.invoice_settings.default_payment_method

    cards = None
    try:
        payment_method = stripe.PaymentMethod.retrieve(default_payment_method)
        card = payment_method.card

        cards = {
            "last4": card.last4,
            "brand": card.brand,
            "exp_month": card.exp_month,
            "exp_year": card.exp_year,
        }
    except:
        pass
    invoices = stripe.Invoice.list(
        customer=profile.strip_costumer_token)
    # print(invoices)
    invoices_list = []
    for i in invoices.auto_paging_iter():
        # Access specific fields directly from the Invoice object
        # account_country = i.account_country
        # account_name = i.account_name
        amount_paid = int(i.amount_paid)/100
        # amount_remaining = i.amount_remaining
        created_timestamp = i.created
        # currency = i.currency
        customer_email = i.customer_email
        customer_name = i.customer_name
        # description = i.description
        invoice_pdf_url = i.invoice_pdf

        # Access line item information
        line_item = i.lines.data[0]

        line_item_amount = int(line_item.amount)/100

        price = line_item.price
        price_unit_amount = int(price.unit_amount)/100

        line_item_description = line_item.description
        line_item_quantity = line_item.quantity

        # Access other invoice information
        invoice_number = i.number
        invoice_status = i.status

        billing_reason_mapping = {
            'subscription_create': 'Subscription Created',
            'subscription_cycle': 'Subscription Renewal',
            'subscription_update': 'Subscription Updated',
            'subscription': 'Subscription Invoice',
            'manual': 'Manual Invoice',
            'upcoming': 'Upcoming Invoice',
            'subscription_threshold': 'Subscription Threshold Invoice',
            'subscription_scheduled': 'Scheduled Invoice',
        }

        # Access the billing reason directly from the Invoice object
        billing_reason = i.billing_reason

        # Map the billing reason to a customer-friendly message
        customer_friendly_billing_reason = billing_reason_mapping.get(
            billing_reason, 'Unknown Reason')

        # Convert the created timestamp to a human-readable date
        created_date = datetime.utcfromtimestamp(
            created_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Create a dictionary with the extracted data
        invoice_info = {

            "InvoiceNumber": invoice_number,
            "CustomerEmail": customer_email,
            "CustomerName": customer_name,
            "CreatedDate": created_date,
            "AmountPaid": amount_paid,
            "ItemAmount": price_unit_amount,
            "ItemQuantity": line_item_quantity,
            "ItemDescription": line_item_description,
            "InvoiceStatus": invoice_status,
            "BillingReason": customer_friendly_billing_reason,
            "InvoicePDF": invoice_pdf_url,
        }

        # print(invoice_info)
        invoices_list.append(invoice_info)

    context = {
        "stripe_public_keys": stripe_public_keys,
        "user": user,
        "card": cards,
        "profile": profile,
        "invoices": invoices_list,

        "life": life,
        "created": created_at_date,
        "current_start": current_period_start_date,
        "current_end": current_period_end_date,
        "number_of_days": number_of_days
    }
    return render(request, 'subscription.html', context)




def change_card(request):
    if request.method == "POST":
        cid = request.POST.get("cid")
        customer = stripe.Customer.retrieve(cid)
        print(customer)
        # Create a new payment method.
  # Create a PaymentMethod using the token.
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "token": request.POST['stripeToken'],
            }
        )

        # Attach the payment method to the customer.
        stripe.PaymentMethod.attach(
            payment_method.id,
            customer=customer.id,
        )

        # Set the customer's default payment method to the newly attached method.
        customer = stripe.Customer.modify(
            customer.id,
            invoice_settings={
                "default_payment_method": payment_method.id,
            }
        )
        customer.save()
        print("Again")
        print(customer)
    return redirect("my_subscriptions")






@login_required
def cancel_subscription(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        customer_token = profile.strip_costumer_token
        subscrition_token = profile.strip_subscription_token

        email = EmailMessage(
            subject=f'Cancel subscription for user {user.id}',
            body=f'''
            user id = {user.id}
            profile = {profile}
            stripe customer token = {customer_token}
            stripe subscription token = {subscrition_token}
            ''',
            from_email=settings.EMAIL1_HOST_USER,
            to=['muhdzarak@gmail.com'],
        )
        email.send()

        return render(request, 'cancel_subscription.html')

    except Exception as e:
        return render(request, '404.html')
# @csrf_exempt
# def stripe_webhook(request):

#     endpoint_secret = end_point_secret

#     event = None
#     payload = request.body
#     sig_header = request.headers['STRIPE_SIGNATURE']

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#         # print(event)

#     except ValueError as e:
#         # Invalid payload
#         raise e

#     if event["type"] == "customer.subscription.updated":
#         session = event["data"]["object"]
#         subscription = session["items"]["data"][0]["subscription"]
#         user_id = session['metadata']['user_id']

#         # print(subscription)
#         user = User.objects.get(id=user_id)
#         is_yearly = session['metadata']['is_yearly']

#         print("Line 227 in Stripe Views")
#         profile_object = Profile.objects.filter(user=user).first()

#         print("This is updated")

#         cs_token = session['customer']
#         properties = session['metadata']['properties']
#         can_add_properties = properties
#         profile_object.can_add = can_add_properties

#         profile_object.is_pro = True
#         profile_object.strip_costumer_token = cs_token
#         profile_object.strip_subscription_token = subscription
#         profile_object.pro_start_date = datetime.now()
#         profile_object.is_yearly = is_yearly
#         # subject = '311Alert Payment Sucessful'

#         profile_object.save()
#         unit_amount = int(session['plan']['amount'])/100
#         total_money = unit_amount * int(properties)

#         if Userpayments.objects.filter(
#                 user=user, payment_is_yearly=is_yearly, payment=total_money, customer_token=profile_object.strip_costumer_token, subscription_token=profile_object.strip_subscription_token).exists():
#             pass
#         else:

#             Userpayments.objects.create(
#                 user=user, payment=total_money, payment_is_yearly=is_yearly, customer_token=profile_object.strip_costumer_token, subscription_token=profile_object.strip_subscription_token)

#     return HttpResponse(status=200)
