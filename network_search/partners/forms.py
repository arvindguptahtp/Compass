from django import forms

from network_search.affiliates.models import Affiliate
from network_search.core import choices
from network_search.core.forms import SearchForm
from network_search.partners.models import Partner


class PartnerAdminForm(forms.ModelForm):

    grade = forms.MultipleChoiceField(choices=choices.GRADE_CHOICES, required=False)
    featured_network = forms.ModelMultipleChoiceField(queryset=Affiliate.objects.all(), required=False)

    class Meta:
        model = Partner
        exclude = ['search_content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['featured_network'].queryset = self.instance.network_use.all()


class PartnerSearchForm(SearchForm):
    """
    Form class for searching partners
    """
