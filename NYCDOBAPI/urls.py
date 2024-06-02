from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import SendPasswordResetEmailView, UserChangePasswordView, AdditionalContactsListView, AdditionalContactView, AdditionalContactDeleteView
from .views import UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView, ComplaintsView, HPDComplaintsListView, HPDComplaintsDetailView, HPDViolationsListView, HPDViolationsDetailView, HPDChargesListView, HPDChargesDetailView, HPDLitigationListView, HPDLitigationDetailView, HPDBedBugReportListView, HPDBedBugReportDetailView, HPDRepairListView, HPDRepairDetailView
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

    path('complaints', ComplaintsView.as_view(),
         name='all_complaints'),
    path('voilations', VoilationsView.as_view(), name='all_voilations'),

    # API Urls for the HPD Data

    # HPD Complaints
    path('hpd-complaints', HPDComplaintsListView.as_view(),
         name='api_hpd_complaints_list_view'),
    path('hpd-complaints/<int:pk>', HPDComplaintsDetailView.as_view(),
         name='api_hpd_complaints_detail_view'),


    # HPD Violations
    path('hpd-violations', HPDViolationsListView.as_view(),
         name='api_hpd_violations_list_view'),
    path('hpd-violations/<int:pk>', HPDViolationsDetailView.as_view(),
         name='api_hpd_violations_detail_view'),


    # HPD Repairs
    path('hpd-repairs', HPDRepairListView.as_view(),
         name='api_hpd_repairs_list_view'),
    path('hpd-repairs/<int:pk>', HPDRepairDetailView.as_view(),
         name='api_hpd_repairs_detail_view'),




    # HPD Charges
    path('hpd-charges', HPDChargesListView.as_view(),
         name='api_hpd_charges_list_view'),
    path('hpd-charges/<int:pk>', HPDChargesDetailView.as_view(),
         name='api_hpd_charges_detail_view'),





    # HPD Litigations
    path('hpd-litigations', HPDLitigationListView.as_view(),
         name='api_hpd_litigations_list_view'),
    path('hpd-litigations/<int:pk>', HPDLitigationDetailView.as_view(),
         name='api_hpd_litigations_detail_view'),



    # HPD BedBugReports
    path('hpd-bedbugreports', HPDBedBugReportListView.as_view(),
         name='api_hpd_bedbugreports_list_view'),
    path('hpd-bedbugreports/<int:pk>', HPDBedBugReportDetailView.as_view(),
         name='api_hpd_bedbugreports_detail_view'),
















    path('properties', PropertyListView.as_view(), name='all_properties'),
    path('adding-property', PropertyView.as_view(), name='adding_property'),
    path('delete-property/<property_id>',
         PropertyDeleteView.as_view(), name='property_delete'),


    path('additionalcontacts', AdditionalContactsListView.as_view(),
         name='all_additionalcontacts'),
    path('add-additionalcontact', AdditionalContactView.as_view(),
         name='add_additionalcontact'),
    path('additionalcontact/<a_c_id>',
         AdditionalContactDeleteView.as_view(), name='additionalcontact_delete'),


    path('contact', ContactView.as_view(), name='api_contact'),
    path('price', PriceView.as_view(), name='api_price'),

]
