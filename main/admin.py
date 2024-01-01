from django.contrib import admin
from . models import *

# Register your models here.


class AddContactsInLineAdmin(admin.TabularInline):
    model = AdditionalContact


class ComplaintsInLineAdmin(admin.TabularInline):
    model = Complaints


class HPDComplaintsInLineAdmin(admin.TabularInline):
    model = HPDComplaints


class violationsInLineAdmin(admin.TabularInline):
    model = Voilation


class HPDVoilationInLineAdmin(admin.TabularInline):
    model = HPDViolations


class HPDChargesInLineAdmin(admin.TabularInline):
    model = HPDCharges


class HPDLitigationInLineAdmin(admin.TabularInline):
    model = HPDLitigation


class HPDRepairInLineAdmin(admin.TabularInline):
    model = HPDRepair


class PropertyInLineAdmin(admin.TabularInline):

    model = Property


class PropertyAdmin(admin.ModelAdmin):
    list_display_links = ['id', 'bin_number',
                          'street', 'house', 'block', 'lott']
    list_editable = ['active_complaints', 'closed_complaints',
                     'active_voilations', 'closed_voilations']
    list_display = ['id', 'bin_number', 'street', 'house',
                    'block', 'lott', 'active_complaints', 'closed_complaints', 'active_voilations', 'closed_voilations']
    search_fields = ['id', 'property_name',  'bin_number', 'borough', 'street', 'house',
                     'block', 'lott']
    list_filter = ['borough', 'street', 'zip']
    inlines = [ComplaintsInLineAdmin,
               violationsInLineAdmin, AddContactsInLineAdmin, HPDComplaintsInLineAdmin, HPDVoilationInLineAdmin, HPDChargesInLineAdmin, HPDLitigationInLineAdmin, HPDRepairInLineAdmin]


class TicketsInLineAdmin(admin.TabularInline):
    model = TicketReply


class TicketsAdmin(admin.ModelAdmin):
    list_editable = ['is_ressolved']
    list_display = ['id', 'user',  'subject', 'is_ressolved']
    search_fields = ['id',  'user__username', ]
    list_filter = ['user', 'is_ressolved']
    inlines = [TicketsInLineAdmin]


class PriceAdmin(admin.ModelAdmin):
    list_editable = ['price_per_month',
                     'price_per_year', 'number_of_properties']
    list_display = ['name', 'price_per_month',
                    'price_per_year', 'number_of_properties']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['is_verified', 'can_add', 'is_pro',
                     'is_yearly', 'pro_start_date', 'profile_image']
    list_display = ['user', 'profile_image',  'can_add',
                    'pro_start_date', 'is_pro', 'is_yearly', 'is_verified']
    search_fields = ['user__username', 'can_add']
    list_filter = ['is_pro', 'is_yearly', 'is_verified']


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'username']

    search_fields = ['username', 'email', 'phone', 'cell', 'address']
    list_filter = ['state', 'city', 'zip']

    inlines = [PropertyInLineAdmin]


class UserPaymentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment',
                    'payment_is_yearly']


admin.site.register(UserCredsSaver)
admin.site.register(AdditionalContact)
admin.site.register(Privacy)
admin.site.register(Terms)
admin.site.register(Price, PriceAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Ticket, TicketsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Userpayments, UserPaymentsAdmin)
