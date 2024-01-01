from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import SendPasswordResetEmailView, UserChangePasswordView, AdditionalContactsListView, AdditionalContactView, AdditionalContactDeleteView
from .views import UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView, ComplaintsView
from .views import VerifyRegisteration, PropertyView, PropertyListView, PropertyDeleteView, ContactView, PriceView
from .views import VoilationsView
urlpatterns = [
    # Authentication routes
    path('register', UserRegistrationView.as_view(), name='api_register'),
    path('verify/', VerifyRegisteration.as_view(),
         name='api_verify_registration'),
    path('login', UserLoginView.as_view(), name='api_login'),
    path('profile/<profile_id>', UserProfileView.as_view(), name='api_profile'),
    path('changepassword', UserChangePasswordView.as_view(),
         name='api_changepassword'),
    
    path('send-reset-password-email', SendPasswordResetEmailView.as_view(),
         name='api_send-reset-password-email'),
    path('reset-password',
         UserPasswordResetView.as_view(), name='api_reset-password'),


    # other routes

    path('complaints', VoilationsView.as_view(), name='all_voilations'),
    path('voilations', ComplaintsView.as_view(), name='all_complaints'),



    path('properties', PropertyListView.as_view(), name='all_properties'),
    path('adding-property', PropertyView.as_view(), name='adding_property'),
    path('delete-property/<property_id>',
         PropertyDeleteView.as_view(), name='property_delete'),


    path('additionalcontacts', AdditionalContactsListView.as_view(), name='all_additionalcontacts'),
    path('add-additionalcontact', AdditionalContactView.as_view(), name='add_additionalcontact'),
    path('additionalcontact/<a_c_id>',
         AdditionalContactDeleteView.as_view(), name='additionalcontact_delete'),


    path('contact', ContactView.as_view(), name='api_contact'),
    path('price', PriceView.as_view(), name='api_price'),

]
