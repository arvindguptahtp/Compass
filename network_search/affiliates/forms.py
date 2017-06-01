from django import forms

from .models import Affiliate


class AffiliateAdminForm(forms.ModelForm):

    class Meta:
        model = Affiliate
        fields = '__all__'
