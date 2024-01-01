# Generated by Django 4.1.3 on 2023-03-15 20:20

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.CharField(max_length=80, unique=True)),
                ('username', models.CharField(max_length=45)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=45)),
                ('company_name', models.CharField(blank=True, max_length=115, null=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=45)),
                ('zip', models.CharField(max_length=45)),
                ('fax', models.CharField(blank=True, max_length=45, null=True)),
                ('cell', models.CharField(blank=True, max_length=45, null=True)),
                ('our_source', models.CharField(blank=True, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('subject', models.CharField(max_length=150)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price_per_month', models.IntegerField(null=True)),
                ('price_per_year', models.IntegerField(null=True)),
                ('number_of_properties', models.IntegerField(null=True)),
                ('is_popular', models.BooleanField(default=False)),
                ('token', models.CharField(blank=True, max_length=500, null=True)),
                ('yearly_token', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privacy', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
                ('borough', models.CharField(max_length=200)),
                ('block', models.CharField(blank=True, max_length=100, null=True)),
                ('lott', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('house', models.CharField(blank=True, max_length=100, null=True)),
                ('bin_number', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('is_ressolved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voilation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voilation_number', models.CharField(blank=True, max_length=600, null=True)),
                ('voilation_type', models.CharField(blank=True, max_length=600, null=True)),
                ('voilation_filedate', models.CharField(blank=True, max_length=600, null=True)),
                ('voilation_dismissaldate', models.CharField(blank=True, max_length=600, null=True)),
                ('voilation_Bageno', models.CharField(blank=True, max_length=600, null=True)),
                ('v_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voilations', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voilations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCredsSaver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=115)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TicketReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField()),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='main.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('auth_token', models.CharField(max_length=500)),
                ('can_add', models.PositiveBigIntegerField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images')),
                ('is_pro', models.BooleanField(default=False)),
                ('is_yearly', models.BooleanField(default=False)),
                ('pro_start_date', models.DateField(blank=True, null=True)),
                ('strip_costumer_token', models.CharField(blank=True, max_length=200, null=True)),
                ('strip_subscription_token', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Complaints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_number', models.CharField(max_length=600)),
                ('complaint_adress', models.CharField(max_length=600)),
                ('complaint_date', models.CharField(max_length=600)),
                ('complaint_category', models.CharField(max_length=600)),
                ('complaint_details', models.CharField(max_length=600)),
                ('complaint_inspection_date', models.CharField(blank=True, max_length=255, null=True)),
                ('complaint_deposition', models.CharField(blank=True, max_length=255, null=True)),
                ('complaint_link', models.CharField(max_length=600)),
                ('complaint_status', models.CharField(max_length=600)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
