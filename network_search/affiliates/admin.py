from django.contrib import admin

from network_search.affiliates.forms import AffiliateAdminForm
from network_search.affiliates.models import Affiliate


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    form = AffiliateAdminForm
