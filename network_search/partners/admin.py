from django.contrib import admin

from network_search.partners.forms import PartnerAdminForm
from network_search.partners.models import Partner
from network_search.partners.models import WebinarLink
from network_search.partners.models import PresentationsLink


class WebinarInline(admin.TabularInline):
    model = WebinarLink
    extra = 1


class PresentationInline(admin.TabularInline):
    model = PresentationsLink
    extra = 1


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    form = PartnerAdminForm
    inlines = [WebinarInline, PresentationInline]
    filter_horizontal = ['network_use', 'featured_network']
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Contact', {
            'fields': ('contact_name', 'contact_title', 'contact_email'),
        }),
        ('General information', {
            'fields': ('website', 'mission', 'overview'),
        }),
        ('Partner details', {
            'fields': ('grade', 'gender', 'organizational_reach', 'student_need', 'tiers_of_service',
                       'setting', 'service_categories', 'tiers_of_evidence', 'is_cost_free',
                       'cost_description', 'is_core_partner', 'network_use', 'featured_network'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).active()
