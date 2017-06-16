from django import forms

from network_search.affiliates import models
from network_search.core import choices
from network_search.core.forms import SearchForm


class AffiliateAdminForm(forms.ModelForm):

    class Meta:
        model = models.Affiliate
        exclude = ['search_content', 'is_removed']


class SchoolAdminForm(forms.ModelForm):
    service_categories = forms.MultipleChoiceField(
        label="Service Categories",
        choices=choices.CoreServices.as_choices(),
        required=False,
    )

    class Meta:
        fields = '__all__'
        model = models.SchoolEOYData


class AffiliateSearchForm(SearchForm):
    """
    Form class for searching partners
    """
