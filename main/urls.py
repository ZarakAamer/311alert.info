from django.urls import path, include
from .views import *
from .property_views import *
from .property_crud import *
from .contact_tickets import *
from .hpd_data import *
from .stripe_views import *
from .registration_views import *
from .dob_data import *


from django.conf.urls import handler404

handler404 = 'main.views.handler404'


urlpatterns = [
    path('', home, name='home'),
    path('pro_home', pro_home, name='pro_home'),
    path('user-properties/', properties_page, name='properties_page'),
    path('property-details/<property_id>',
         property_details_page, name='property_details'),
    path('edit-property-page/<property_id>',
         edit_property_page, name='edit_property_page'),
    path('property-search', property_search_page,
         name='property_search_page'),
    path('pricing', princing, name='price'),
    path('adding-property', add_property, name='addproperty'),
    path('edit-property/<property_id>',
         edit_property, name='edit_property'),
    path('edit-contact/<int:contact_id>',
         edit_contact, name='edit_contact'),
    path('add-property', add_properties,
         name='add_property'),
    path('delete_street_property/<int:pro_id>',
         delete_street_property, name='delete_street_property'),
    path('contact-us', contact, name='contact'),
    path('contacting', contact_process, name="contacting"),
    path('my-tickets', tickets, name='tickets'),
    path('ticket/id/<id>', ticket_details, name='ticket_details'),
    path('ticket/ressolved/<id>', ticket_ressolved, name='ticket_ressolved'),
    path('ticket/reply', reply_ticket, name='reply_ticket'),
    path('create-ticket', ticket, name='ticket'),
    path('creating-ticket', ticket_process, name="creating"),
    path('privacy-and-policy', privacy_policy, name="privacy"),
    path('terms-of-use', terms_of_use, name="terms"),


    # -------------------dob urls----------------
    path('dob_data', dob_data, name='dob_data'),

    path('complaints', complaints,
         name='complaints'),
    path('complaints-by-property/<id>', complaints_by_property,
         name='complaints_by_property'),
    path('violations/', violations,
         name='violations'),
    path('violations-by-property/<id>', violations_by_property,
         name='violations_by_property'),

    # -------------------hpd urls----------------

    path('hpd-data', hpd_data, name='hpd_data'),
    path('hpd-complaints', hpd_complaints,
         name='hpd_complaints'),
    path('hpd-complaints-by-property/<id>', hpd_complaints_by_property,
         name='hpd_complaints_by_property'),

    path('hpd-violations', hpd_violations,
         name='hpd_violations'),
    path('hpd-violations-by-property/<id>', hpd_violations_by_property,
         name='hpd_violations_by_property'),


    path('hpd-charges', hpd_charges,
         name='hpd_charges'),
    path('hpd-charges-by-property/<id>', hpd_charges_by_property,
         name='hpd_charges_by_property'),


    path('hpd-litigations', hpd_ligitations,
         name='hpd_litigations'),
    path('hpd-litigations-by-property/<id>', hpd_ligitations_by_property,
         name='hpd_litigations_by_property'),

    path('hpd-repair-vacate-orders', hpd_repais_orders,
         name='hpd_repairs'),
    path('hpd-repair-vacate-orders-by-property/<id>', hpd_repais_orders_by_property,
         name='hpd_repairs_by_property'),

    path('hpd-bedbug-reports', hpd_bedbug,
         name='hpd_bedbug'),
    path('hpd-bedbug-reports-by-property/<id>', hpd_bedbug_by_property,
         name='hpd_bedbug_by_property'),
    # -------------------accounts urls----------------




    path('register-attempt', register, name='register'),
    path('login-attempt', login_attempt, name='login'),
    path('logout-attempt', logout_attempt, name='logout'),
    path('forgot-password/', ForgetPassword, name="forget_password"),
    path('password-reset-verification/<auth_token>/',
         ChangePassword, name="change_password"),
    path('verify', verify, name='verify'),
    path('membership-process', become_pro, name='pro'),
    path('choose-package/<param1>', payment_after_registeration,
         name='payment_after_registeration'),
    path('paying', payment_at_registration,
         name='payment_at_registration'),
    path('verify-email', verify_email, name='verify_email'),
    path('change-subscription', change_subscription,
         name='change_subscription'),
    path('success/paid', success_second, name='success_2'),
    path('success/payment/done', success_third, name='success_3'),
    path('success', success, name='success'),
    path('cancel', cancel, name='cancel'),
    path('twenty-plus-properties', twenty_plus, name='twenty_plus'),
    path('user-is-pro', already_pro, name='pro_user'),
    path('edit-user-information', edit_user_information,
         name='edit_user_information'),
    path('update-profile-info', update_profile_info,
         name='update_profile_info'),
    path('update-profile-image', change_profile_image,
         name='change_profile_image'),
    path('update-password', update_password_info,
         name='update_password_info'),
    path('update-subscription', update_subscription,
         name='update_subscription'),
    path('user-profile', user_prof, name='user_prof'),
    path('my-payments', my_subscriptions, name="my_subscriptions"),
    path('change-card', change_card, name="change_card"),
    path('cancel-subscription', cancel_subscription, name="cancel_subscription"),
]
