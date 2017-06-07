from django.contrib import admin

from network_search.programs.models import Program, NationalDatabase, RelatedResource
from network_search.programs.forms import ProgramAdminForm


class NationalDatabaseInline(admin.TabularInline):
    model = NationalDatabase
    extra = 1


class RelatedResourceInline(admin.TabularInline):
    model = RelatedResource
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramAdminForm
    filter_horizontal = ['network_use']
    inlines = [NationalDatabaseInline, RelatedResourceInline]

    fieldsets = [
        (None, {
            'fields': ['name'],
        }),
        ('Program information', {
            'fields': ['summary', 'description'],
        }),
        ('Target population', {
            'fields': ['grade', 'gender',  'race', 'region',
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
