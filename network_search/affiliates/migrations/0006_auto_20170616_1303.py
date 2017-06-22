# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 18:03
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0005_auto_20170615_0442'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studenteoydata',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='studenteoydata',
            name='affiliate',
        ),
        migrations.RemoveField(
            model_name='studenteoydata',
            name='year',
        ),
        migrations.AlterModelOptions(
            name='schooleoydata',
            options={'verbose_name': 'School and Student EOY Data', 'verbose_name_plural': 'School and Student EOY Data'},
        ),
        migrations.AddField(
            model_name='affiliate',
            name='affiliate_location',
            field=models.CharField(default=' ', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='affiliateeoydata',
            name='school_districts',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='cis_model_school',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='name',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='service_categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_case_managed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_american_indian',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_asian',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_black',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_hispanic',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_other',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_two_or_more_races',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_unknown',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_female_white',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_grade_12_dropped_out',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_grade_12_graduated',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_grade_12_other',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_grade_12_retained',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_grade_12_transferred',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_grade_12_unknown',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_k_11_dropped_out',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_k_11_other',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_k_11_promoted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_k_11_retained',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_k_11_transferred',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_k_11_unknown',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_american_indian',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_asian',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_black',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_hispanic',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_other',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_two_or_more_races',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_unknown',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_male_white',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_adjudicated_youth',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_child_of_military',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_ell',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_foster',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_frpl',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_gang',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_homeless',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_incarcerated_parent',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_lgbt',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_pregnant_parenting',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_special_education',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_served_substance_abuse',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='schooleoydata',
            name='students_unknown_race_gender',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='StudentEOYData',
        ),
    ]