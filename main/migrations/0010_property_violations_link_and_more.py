# Generated by Django 4.1.7 on 2023-05-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_complaints_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='violations_link',
            field=models.CharField(blank=True, max_length=1400, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='active_complaints',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='active_voilations',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='closed_complaints',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='closed_voilations',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
