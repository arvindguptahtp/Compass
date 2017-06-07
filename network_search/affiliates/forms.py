from django import forms

from network_search.affiliates.models import Affiliate
from network_search.core.forms import SearchForm


class AffiliateAdminForm(forms.ModelForm):

    class Meta:
        model = Affiliate
        fields = '__all__'


class AffiliateSearchForm(SearchForm):
    """
    Form class for searching partners
    """
