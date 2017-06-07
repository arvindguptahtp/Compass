from django import forms

from network_search.core.forms import SearchForm
from network_search.affiliates.models import Affiliate


class AffiliateAdminForm(forms.ModelForm):

    class Meta:
        model = Affiliate
        exclude = ['search_content', 'is_removed']


class AffiliateSearchForm(SearchForm):
    """
    Form class for searching partners
    """
