# Generated by Django 4.1.7 on 2023-04-28 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_property_active_complaints_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='active_voilations',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='closed_voilations',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='voilation',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
