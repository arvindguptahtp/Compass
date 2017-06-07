from django import forms

from .models import Affiliate


class AffiliateAdminForm(forms.ModelForm):

    class Meta:
        model = Affiliate
        fields = '__all__'


class AffiliateSearchForm(forms.Form):
    """
    Form class for searching partners
    """
    q = forms.CharField(required=False)
