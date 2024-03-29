# Generated by Django 4.1.3 on 2023-04-01 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_ticket_answer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaints',
            old_name='complaint_deposition',
            new_name='disposition_date',
        ),
        migrations.RenameField(
            model_name='complaints',
            old_name='complaint_inspection_date',
            new_name='inspection_date',
        ),
        migrations.RenameField(
            model_name='voilation',
            old_name='voilation_Bageno',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='voilation',
            old_name='voilation_dismissaldate',
            new_name='device_number',
        ),
        migrations.RenameField(
            model_name='voilation',
            old_name='voilation_filedate',
            new_name='disposition_comments',
        ),
        migrations.RenameField(
            model_name='voilation',
            old_name='voilation_number',
            new_name='disposition_date',
        ),
        migrations.RenameField(
            model_name='voilation',
            old_name='voilation_type',
            new_name='ecb_number',
        ),
        migrations.RemoveField(
            model_name='complaints',
            name='complaint_adress',
        ),
        migrations.RemoveField(
            model_name='complaints',
            name='complaint_date',
        ),
        migrations.RemoveField(
            model_name='complaints',
            name='complaint_details',
        ),
        migrations.RemoveField(
            model_name='complaints',
            name='complaint_link',
        ),
        migrations.RemoveField(
            model_name='complaints',
            name='complaint_status',
        ),
        migrations.RemoveField(
            model_name='voilation',
            name='v_link',
        ),
        migrations.AddField(
            model_name='complaints',
            name='community_board',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='complaints',
            name='date_entered',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='complaints',
            name='disposition_code',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='complaints',
            name='status',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='complaints',
            name='unit',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='voilation',
            name='issue_date',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='voilation',
            name='number',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='voilation',
            name='violation_category',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='voilation',
            name='violation_number',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='voilation',
            name='violation_type',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='complaint_category',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='complaint_number',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
