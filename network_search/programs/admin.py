from django.contrib import admin

from network_search.programs.forms import ProgramAdminForm
from network_search.programs.models import Program
from network_search.programs.models import RelatedResource
from network_search.programs.models import NationalDatabase
from network_search.programs.models import AdditionalResource


class AdditionalResourceInline(admin.TabularInline):
    model = AdditionalResource
    extra = 0


class NationalDatabaseInline(admin.TabularInline):
    model = NationalDatabase
    extra = 0


class RelatedResourceInline(admin.TabularInline):
    model = RelatedResource
    extra = 0


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramAdminForm
    filter_horizontal = ['network_use']
    inlines = [NationalDatabaseInline, RelatedResourceInline, AdditionalResourceInline]

    fieldsets = [
        (None, {
            'fields': ['name'],
        }),
        ('Program information', {
            'fields': ['summary', 'description', 'program_weblink'],
        }),
        ('Target population', {
            'fields': ['grade', 'gender', 'race', 'region', 'region_other',
                       'student_need', 'student_characteristics'],
        }),
        ('Program characteristics', {
            'fields': ['tiers_of_service', 'setting', 'national_partner',
                       'service_categories', 'is_cost_free', 'cost_description',
                       'assessment_available', 'assessment_info'],
        }),
        ('Use in network', {
            'fields': ['network_use', 'featured_network'],
        }),
        ('Evidence base', {
            'fields': ['outcomes', 'tiers_of_evidence'],
        }),
    ]
