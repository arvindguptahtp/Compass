from django.contrib import admin

from network_search.affiliates.forms import AffiliateAdminForm
from network_search.affiliates import models


@admin.register(models.Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    form = AffiliateAdminForm


@admin.register(models.EndOfYear)
class EndOfYearAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']


@admin.register(models.AffiliateEOYData)
class AffiliateEOYAdmin(admin.ModelAdmin):
    raw_id_fields = ['affiliate']


@admin.register(models.SchoolEOYData)
class SchoolEOYAdmin(admin.ModelAdmin):
    raw_id_fields = ['affiliate']


@admin.register(models.StudentEOYData)
class StudentEOYAdmin(admin.ModelAdmin):
    raw_id_fields = ['affiliate']
