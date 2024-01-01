# Generated by Django 4.1.7 on 2023-10-21 01:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_hpdcomplaints'),
    ]

    operations = [
        migrations.CreateModel(
            name='HPDViolations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('violationid', models.CharField(blank=True, max_length=100, null=True)),
                ('buildingid', models.CharField(blank=True, max_length=100, null=True)),
                ('registrationid', models.CharField(blank=True, max_length=100, null=True)),
                ('story', models.CharField(blank=True, max_length=100, null=True)),
                ('violations_class', models.CharField(blank=True, max_length=100, null=True)),
                ('inspectiondate', models.CharField(blank=True, max_length=100, null=True)),
                ('approveddate', models.CharField(blank=True, max_length=100, null=True)),
                ('originalcertifybydate', models.CharField(blank=True, max_length=100, null=True)),
                ('originalcorrectbydate', models.CharField(blank=True, max_length=100, null=True)),
                ('ordernumber', models.CharField(blank=True, max_length=100, null=True)),
                ('novid', models.CharField(blank=True, max_length=100, null=True)),
                ('novdescription', models.TextField(blank=True, null=True)),
                ('novissueddate', models.CharField(blank=True, max_length=100, null=True)),
                ('currentstatusid', models.CharField(blank=True, max_length=100, null=True)),
                ('currentstatus', models.CharField(blank=True, max_length=100, null=True)),
                ('currentstatusdate', models.CharField(blank=True, max_length=100, null=True)),
                ('novtype', models.CharField(blank=True, max_length=100, null=True)),
                ('violationstatus', models.CharField(blank=True, max_length=100, null=True)),
                ('rentimpairing', models.CharField(blank=True, max_length=100, null=True)),
                ('communityboard', models.CharField(blank=True, max_length=100, null=True)),
                ('councildistrict', models.CharField(blank=True, max_length=100, null=True)),
                ('censustract', models.CharField(blank=True, max_length=100, null=True)),
                ('nta', models.CharField(blank=True, max_length=100, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hpd_violations', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hpd_violations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'HPD Voilation',
                'verbose_name_plural': 'HPD violations',
            },
        ),
        migrations.CreateModel(
            name='HPDRepair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_id', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_id', models.CharField(blank=True, max_length=100, null=True)),
                ('vacate_order_number', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_vacate_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('vacate_type', models.CharField(blank=True, max_length=100, null=True)),
                ('vacate_effective_date', models.CharField(blank=True, max_length=100, null=True)),
                ('actual_rescind_date', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_vacated_units', models.CharField(blank=True, max_length=100, null=True)),
                ('postoce', models.CharField(blank=True, max_length=100, null=True)),
                ('community_board', models.CharField(blank=True, max_length=100, null=True)),
                ('council_district', models.CharField(blank=True, max_length=100, null=True)),
                ('census_tract', models.CharField(blank=True, max_length=100, null=True)),
                ('nta', models.CharField(blank=True, max_length=200, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hpd_repairs', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hpd_repairs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HPDLitigation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('litigationid', models.CharField(blank=True, max_length=100, null=True)),
                ('buildingid', models.CharField(blank=True, max_length=100, null=True)),
                ('casetype', models.CharField(blank=True, max_length=100, null=True)),
                ('caseopendate', models.CharField(blank=True, max_length=100, null=True)),
                ('casestatus', models.CharField(blank=True, max_length=100, null=True)),
                ('casejudgement', models.CharField(blank=True, max_length=100, null=True)),
                ('respondent', models.TextField(blank=True, null=True)),
                ('community_district', models.CharField(blank=True, max_length=100, null=True)),
                ('council_district', models.CharField(blank=True, max_length=100, null=True)),
                ('census_tract', models.CharField(blank=True, max_length=100, null=True)),
                ('nta', models.CharField(blank=True, max_length=100, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hpd_litigations', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hpd_litigations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HPDCharges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feeid', models.CharField(blank=True, max_length=100, null=True)),
                ('buildingid', models.CharField(blank=True, max_length=100, null=True)),
                ('lifecycle', models.CharField(blank=True, max_length=100, null=True)),
                ('feetypeid', models.CharField(blank=True, max_length=100, null=True)),
                ('feetype', models.CharField(blank=True, max_length=100, null=True)),
                ('feesourcetypeid', models.CharField(blank=True, max_length=100, null=True)),
                ('feesourcetype', models.CharField(blank=True, max_length=100, null=True)),
                ('feesourceid', models.CharField(blank=True, max_length=100, null=True)),
                ('feeissueddate', models.CharField(blank=True, max_length=100, null=True)),
                ('feeamount', models.CharField(blank=True, max_length=100, null=True)),
                ('dofaccounttype', models.CharField(blank=True, max_length=100, null=True)),
                ('community_board', models.CharField(blank=True, max_length=100, null=True)),
                ('council_district', models.CharField(blank=True, max_length=100, null=True)),
                ('census_tract', models.CharField(blank=True, max_length=100, null=True)),
                ('nta', models.CharField(blank=True, max_length=100, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hpd_charges', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hpd_charges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HPDBedBugReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_id', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_id', models.CharField(blank=True, max_length=100, null=True)),
                ('postcode', models.CharField(blank=True, max_length=100, null=True)),
                ('of_dwelling_units', models.CharField(blank=True, max_length=100, null=True)),
                ('infested_dwelling_unit_count', models.CharField(blank=True, max_length=100, null=True)),
                ('eradicated_unit_count', models.CharField(blank=True, max_length=100, null=True)),
                ('re_infested_dwelling_unit', models.TextField(blank=True, null=True)),
                ('filing_date', models.CharField(blank=True, max_length=100, null=True)),
                ('filing_period_start_date', models.CharField(blank=True, max_length=100, null=True)),
                ('filling_period_end_date', models.CharField(blank=True, max_length=100, null=True)),
                ('community_board', models.CharField(blank=True, max_length=100, null=True)),
                ('city_council_district', models.CharField(blank=True, max_length=100, null=True)),
                ('census_tract_2010', models.CharField(blank=True, max_length=100, null=True)),
                ('nta', models.CharField(blank=True, max_length=100, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hpd_bedbugs', to='main.property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hpd_bedbugs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]