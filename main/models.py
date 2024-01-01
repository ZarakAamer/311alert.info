
from django.conf import settings
from django.db import models


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, EmailMessage


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    company_name = models.CharField(max_length=115, null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    zip = models.CharField(max_length=45)
    fax = models.CharField(max_length=45, null=True, blank=True)
    cell = models.CharField(max_length=45, null=True, blank=True)
    our_source = models.CharField(max_length=200, null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{str(self.username)} + {str(self.email)}"


class UserCredsSaver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=115)

    def __str__(self):
        return self.email


class Userpayments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments")
    payment_is_yearly = models.BooleanField(default=False)
    payment = models.IntegerField(default=0)
    customer_token = models.CharField(max_length=255, null=True, blank=True)
    subscription_token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.email} totatl payment ${self.payment}"

    class Meta:
        verbose_name = 'User Payment'
        verbose_name_plural = 'User Payments'


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="profile")
    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=500)
    can_add = models.PositiveBigIntegerField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profile_images", null=True, blank=True)

    # is_month = models.BooleanField(default=False)
    # is_year = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    is_yearly = models.BooleanField(default=False)
    pro_start_date = models.DateField(null=True, blank=True)
    strip_costumer_token = models.CharField(
        max_length=200,  null=True, blank=True)
    strip_subscription_token = models.CharField(
        max_length=200,  null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Property(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")
    property_name = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    borough = models.CharField(max_length=200)
    block = models.CharField(max_length=100, null=True, blank=True)
    lott = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    house = models.CharField(max_length=100, null=True, blank=True)
    bin_number = models.CharField(max_length=200, null=True, blank=True)

    closed_complaints = models.CharField(
        max_length=200, null=True, blank=True, default=0)
    active_complaints = models.CharField(
        max_length=200, null=True, blank=True, default=0)
    closed_voilations = models.CharField(
        max_length=200, null=True, blank=True, default=0)
    active_voilations = models.CharField(
        max_length=200, null=True, blank=True, default=0)
    complaints_link = models.CharField(max_length=1400, null=True, blank=True)
    violations_link = models.CharField(max_length=1400, null=True, blank=True)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.user.username


class AdditionalContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="contacts", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f" {self.name}:  {self.property.house}, {self.property.street}"

    class Meta:
        verbose_name = 'Additional Contact'
        verbose_name_plural = 'Additional Contacts'


class Complaints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="complaints", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="complaints")
    complaint_number = models.CharField(max_length=600, null=True, blank=True)
    date_entered = models.CharField(max_length=600, null=True, blank=True)
    complaint_category = models.CharField(
        max_length=600, null=True, blank=True)
    community_board = models.CharField(max_length=600, null=True, blank=True)
    disposition_code = models.CharField(max_length=600, null=True, blank=True)
    unit = models.CharField(max_length=600, null=True, blank=True)
    inspection_date = models.CharField(
        max_length=255, blank=True, null=True)
    disposition_date = models.CharField(
        max_length=255, blank=True, null=True)
    link = models.URLField(max_length=1200, blank=True, null=True)
    status = models.CharField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.complaint_number

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'


class Voilation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="voilations", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="voilations")
    number = models.CharField(max_length=600, blank=True, null=True)
    violation_number = models.CharField(max_length=600, blank=True, null=True)
    violation_type = models.CharField(max_length=600, blank=True, null=True)
    violation_category = models.CharField(
        max_length=600, blank=True, null=True)
    issue_date = models.CharField(
        max_length=600, blank=True, null=True)
    disposition_date = models.CharField(
        max_length=600, blank=True, null=True)
    disposition_comments = models.CharField(
        max_length=600, blank=True, null=True)
    description = models.CharField(max_length=600, blank=True, null=True)
    device_number = models.CharField(max_length=600, blank=True, null=True)
    ecb_number = models.CharField(max_length=600, blank=True, null=True)
    link = models.URLField(max_length=1200,  blank=True, null=True)

    def __str__(self):
        return str(self.property.bin_number)

    class Meta:
        verbose_name = 'Voilation'
        verbose_name_plural = 'Voilations'


class HPDComplaints(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="hpd_complaints", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="hpd_complaints")

    received_date = models.CharField(max_length=100, null=True, blank=True)
    problem_id = models.CharField(max_length=100, null=True, blank=True)
    complaint_id = models.CharField(max_length=100, null=True, blank=True)
    building_id = models.CharField(max_length=100, null=True, blank=True)
    apartment = models.CharField(max_length=100, null=True, blank=True)
    community_board = models.CharField(max_length=100, null=True, blank=True)
    unit_type = models.CharField(max_length=100, null=True, blank=True)
    space_type = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    major_category = models.CharField(max_length=100, null=True, blank=True)
    minor_category = models.CharField(max_length=100, null=True, blank=True)
    problem_code = models.CharField(max_length=100, null=True, blank=True)
    complaint_status = models.CharField(max_length=100, null=True, blank=True)
    complaint_status_date = models.CharField(
        max_length=100, null=True, blank=True)
    problem_status = models.CharField(max_length=100, null=True, blank=True)
    problem_status_date = models.CharField(
        max_length=100, null=True, blank=True)
    status_description = models.TextField(null=True, blank=True)
    council_district = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.complaint_id)

    class Meta:
        verbose_name = 'HPD Complaint'
        verbose_name_plural = 'HPD Complaints'


class HPDViolations(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="hpd_violations", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="hpd_violations")
    violationid = models.CharField(max_length=100, null=True, blank=True)
    buildingid = models.CharField(max_length=100, null=True, blank=True)
    registrationid = models.CharField(max_length=100, null=True, blank=True)
    story = models.CharField(max_length=100, null=True, blank=True)
    violations_class = models.CharField(max_length=100, null=True, blank=True)
    inspectiondate = models.CharField(max_length=100, null=True, blank=True)
    approveddate = models.CharField(max_length=100, null=True, blank=True)
    originalcertifybydate = models.CharField(
        max_length=100, null=True, blank=True)
    originalcorrectbydate = models.CharField(
        max_length=100, null=True, blank=True)
    ordernumber = models.CharField(max_length=100, null=True, blank=True)
    novid = models.CharField(max_length=100, null=True, blank=True)
    novdescription = models.TextField(null=True, blank=True)
    novissueddate = models.CharField(max_length=100, null=True, blank=True)
    currentstatusid = models.CharField(max_length=100, null=True, blank=True)
    currentstatus = models.CharField(max_length=100, null=True, blank=True)
    currentstatusdate = models.CharField(max_length=100, null=True, blank=True)
    novtype = models.CharField(max_length=100, null=True, blank=True)
    violationstatus = models.CharField(max_length=100, null=True, blank=True)
    rentimpairing = models.CharField(max_length=100, null=True, blank=True)
    communityboard = models.CharField(max_length=100, null=True, blank=True)
    councildistrict = models.CharField(max_length=100, null=True, blank=True)
    censustract = models.CharField(max_length=100, null=True, blank=True)
    nta = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.violationid

    class Meta:
        verbose_name = 'HPD Voilation'
        verbose_name_plural = 'HPD violations'


class HPDCharges(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="hpd_charges", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="hpd_charges")
    feeid = models.CharField(max_length=100, null=True, blank=True)
    buildingid = models.CharField(max_length=100, null=True, blank=True)
    lifecycle = models.CharField(max_length=100, null=True, blank=True)
    feetypeid = models.CharField(max_length=100, null=True, blank=True)
    feetype = models.CharField(max_length=100, null=True, blank=True)
    feesourcetypeid = models.CharField(max_length=100, null=True, blank=True)
    feesourcetype = models.CharField(max_length=100, null=True, blank=True)
    feesourceid = models.CharField(max_length=100, null=True, blank=True)
    feeissueddate = models.CharField(max_length=100, null=True, blank=True)
    feeamount = models.CharField(max_length=100, null=True, blank=True)
    dofaccounttype = models.CharField(max_length=100, null=True, blank=True)
    community_board = models.CharField(max_length=100, null=True, blank=True)
    council_district = models.CharField(max_length=100, null=True, blank=True)
    census_tract = models.CharField(max_length=100, null=True, blank=True)
    nta = models.CharField(max_length=100, null=True, blank=True)


class HPDLitigation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="hpd_litigations", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="hpd_litigations")
    litigationid = models.CharField(max_length=100, null=True, blank=True)
    buildingid = models.CharField(max_length=100, null=True, blank=True)
    casetype = models.CharField(max_length=100, null=True, blank=True)
    caseopendate = models.CharField(max_length=100, null=True, blank=True)
    casestatus = models.CharField(max_length=100, null=True, blank=True)
    casejudgement = models.CharField(max_length=100, null=True, blank=True)
    respondent = models.TextField(null=True, blank=True)
    community_district = models.CharField(
        max_length=100, null=True, blank=True)
    council_district = models.CharField(max_length=100, null=True, blank=True)
    census_tract = models.CharField(max_length=100, null=True, blank=True)
    nta = models.CharField(max_length=100, null=True, blank=True)


class HPDRepair(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="hpd_repairs", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="hpd_repairs")
    building_id = models.CharField(max_length=100, null=True, blank=True)
    registration_id = models.CharField(max_length=100, null=True, blank=True)
    vacate_order_number = models.CharField(
        max_length=100, null=True, blank=True)
    primary_vacate_reason = models.CharField(
        max_length=100, null=True, blank=True)
    vacate_type = models.CharField(max_length=100, null=True, blank=True)
    vacate_effective_date = models.CharField(
        max_length=100, null=True, blank=True)
    actual_rescind_date = models.CharField(
        max_length=100, null=True, blank=True)
    number_of_vacated_units = models.CharField(
        max_length=100, null=True, blank=True)
    postoce = models.CharField(max_length=100, null=True, blank=True)
    community_board = models.CharField(max_length=100, null=True, blank=True)
    council_district = models.CharField(max_length=100, null=True, blank=True)
    census_tract = models.CharField(max_length=100, null=True, blank=True)
    nta = models.CharField(max_length=200, null=True, blank=True)


class HPDBedBugReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="hpd_bedbugs", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="hpd_bedbugs")
    building_id = models.CharField(max_length=100, null=True, blank=True)
    registration_id = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    of_dwelling_units = models.CharField(max_length=100, null=True, blank=True)
    infested_dwelling_unit_count = models.CharField(
        max_length=100, null=True, blank=True)
    eradicated_unit_count = models.CharField(
        max_length=100, null=True, blank=True)
    re_infested_dwelling_unit = models.TextField(null=True, blank=True)
    filing_date = models.CharField(
        max_length=100, null=True, blank=True)
    filing_period_start_date = models.CharField(
        max_length=100, null=True, blank=True)
    filling_period_end_date = models.CharField(
        max_length=100, null=True, blank=True)
    community_board = models.CharField(max_length=100, null=True, blank=True)
    city_council_district = models.CharField(
        max_length=100, null=True, blank=True)
    census_tract_2010 = models.CharField(max_length=100, null=True, blank=True)
    nta = models.CharField(max_length=100, null=True, blank=True)



class Price(models.Model):
    name = models.CharField(max_length=100)
    price_per_month = models.CharField(max_length=200, null=True, blank=True)
    price_per_year = models.CharField(max_length=200, null=True, blank=True)
    number_of_properties = models.IntegerField(null=True)
    product_token = models.CharField(max_length=500, null=True, blank=True)
    first_month_token = models.CharField(max_length=500, null=True, blank=True)
    subsequent_months_token = models.CharField(
        max_length=500, null=True, blank=True)

    first_year_token = models.CharField(max_length=500, null=True, blank=True)
    subsequent_years_token = models.CharField(
        max_length=500, null=True, blank=True)
    price_change_to_year = models.CharField(
        max_length=500, null=True, blank=True)
    price_change_to_month = models.CharField(
        max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}  +  {self.email}"


class Ticket(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tickets")
    subject = models.CharField(max_length=100)
    description = models.TextField()
    is_ressolved = models.BooleanField(default=False)
    answer = RichTextUploadingField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.username}"


class TicketReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="replies")
    description = models.TextField()
    answer = RichTextUploadingField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.username}"


@receiver(post_save, sender=TicketReply)
def send_answer_email(sender, instance, **kwargs):
    """
    Sends an email to the user when a TicketReply is saved and the answer field has been updated.
    """
    if instance.answer and not kwargs.get('created'):
        subject = 'Your ticket has been updated'
        message = 'Your ticket has been updated with the following answer:\n\n{}'.format(
            instance.answer)
        message = instance.answer
        subject = subject

        context = {
            "id": instance.tick.id,
            "fname": instance.user.first_name,
            "details": message
        }

        from_email = settings.EMAIL1_HOST_USER

        templ = get_template('ticketanswer.txt')
        messageing = templ.render(context)
        emailnew = EmailMultiAlternatives(
            subject, messageing, from_email, [instance.user.email])

        emailnew.content_subtype = 'html'
        emailnew.send()


@receiver(post_save, sender=Ticket)
def send_answer_email(sender, instance, **kwargs):
    """
    Sends an email to the user when a TicketReply is saved and the answer field has been updated.
    """
    if instance.answer and not kwargs.get('created'):
        subject = 'Your ticket has been updated'
        message = instance.answer
        subject = subject

        context = {
            "id": instance.id,
            "fname": instance.user.first_name,
            "details": message
        }

        from_email = settings.EMAIL1_HOST_USER

        templ = get_template('ticketanswer.txt')
        messageing = templ.render(context)
        emailnew = EmailMultiAlternatives(
            subject, messageing, from_email, [instance.user.email])

        emailnew.content_subtype = 'html'
        emailnew.send()
        print(subject)
    elif instance.is_ressolved and not kwargs.get('created'):
        subject = 'Your ticket has been updated'
        message = 'Your ticket has been marked as Ressolved'
        print(subject)
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL1_HOST_USER,
            to=[instance.user.email]
        )
        email.send()
        print(subject)


class Privacy(models.Model):
    privacy = RichTextUploadingField()

    def __str__(self):
        return f"Privacy Version {self.id}"


class Terms(models.Model):
    terms = RichTextUploadingField()

    def __str__(self):
        return f"Terms Version {self.id}"

    class Meta:
        verbose_name = 'Terms of use'
        verbose_name_plural = 'Terms of use'


class Upload(models.Model):
    file = models.FileField(upload_to="komal")