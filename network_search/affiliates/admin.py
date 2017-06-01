from django.contrib import admin

from .models import Affiliate
from .forms import AffiliateAdminForm


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    form = AffiliateAdminForm
