# Generated by Django 4.1.7 on 2023-04-16 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_additionalcontact_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='active_complaints',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='closed_complaints',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='complaints_link',
            field=models.CharField(blank=True, max_length=1400, null=True),
        ),
    ]
