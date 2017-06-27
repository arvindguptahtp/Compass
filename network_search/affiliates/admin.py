from django.contrib import admin

from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from network_search.affiliates import forms
from network_search.affiliates import models


@admin.register(models.ExcelUpload)
class AffiliateUploadAdmin(admin.ModelAdmin):
    list_display = ['year', 'status', 'created', 'data_file']
    actions = ['copy_import']

    def copy_import(self, request, queryset):
        try:
            original = queryset.get()
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            messages.error(request, "Select 1 and only 1 upload to copy")
            return

        models.ExcelUpload.objects.create(
            year=original.year,
            data_file=original.data_file
        )
        messages.success(request, "Starting new data import.")

    copy_import.short_description = "Duplicate and rerun an import"


@admin.register(models.Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    form = forms.AffiliateAdminForm
    list_display = ('name', 'state')
    search_fields = ('name', 'state')


@admin.register(models.EndOfYear)
class EndOfYearAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']


@admin.register(models.AffiliateEOYData)
class AffiliateEOYAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'year')
    search_fields = ('affiliate__name',)
    raw_id_fields = ['affiliate']


@admin.register(models.SchoolEOYData)
class SchoolEOYAdmin(admin.ModelAdmin):
    # list_display = ('name', 'affiliate', 'year')
    search_fields = ['name', 'affiliate_data__affiliate__name']
    raw_id_fields = ['affiliate_data']
    form = forms.SchoolAdminForm
    fieldsets = (
        (None, {
            'fields': ['affiliate_data'],
        }),
        ('School', {
            'fields': ['name', 'site_type', 'location', 'location_model', 'students_case_managed', 'students_total',
                       'partners'],
        }),
        ('Students race and gender', {
            'fields': [
                'students_female_american_indian', 'students_female_asian', 'students_female_black',
                'students_female_hispanic', 'students_female_white', 'students_female_two_or_more_races',
                'students_female_other', 'students_female_unknown', 'students_male_american_indian',
                'students_male_asian', 'students_male_black', 'students_male_hispanic',
                'students_male_white', 'students_male_two_or_more_races', 'students_male_other',
                'students_male_unknown', 'students_unknown_race_gender',
            ],
        }),
        ('Student performance', {
            'fields': [
                'students_k_11_promoted', 'students_k_11_retained', 'students_k_11_dropped_out',
                'students_k_11_transferred', 'students_k_11_ged',
                'students_k_11_expelled', 'students_k_11_incarcerated', 'students_k_11_deceased',
                'students_k_11_other', 'students_k_11_unknown',
                'students_grade_12_graduated', 'students_grade_12_retained', 'students_grade_12_dropped_out',
                'students_grade_12_transferred',
                'students_grade_12_ged',
                'students_grade_12_expelled',
                'students_grade_12_incarcerated',
                'students_grade_12_deceased',
                'students_grade_12_other', 'students_grade_12_unknown'
            ]
        }),
        ('Students served', {
            'fields': [
                'students_served_frpl', 'students_served_ell', 'students_served_foster',
                'students_served_homeless', 'students_served_lgbt', 'students_served_pregnant_parenting',
                'students_served_special_education', 'students_served_substance_abuse',
                'students_served_adjudicated_youth', 'students_served_child_of_military',
                'students_served_gang', 'students_served_incarcerated_parent'
            ]
        }),
    )
