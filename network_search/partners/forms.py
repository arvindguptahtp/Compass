from django import forms

from network_search.core import choices
from network_search.core.forms import SearchForm
from network_search.partners.models import Partner
from network_search.affiliates.models import Affiliate


class PartnerAdminForm(forms.ModelForm):

    grade = forms.MultipleChoiceField(choices=choices.GRADES, required=False)
    featured_network = forms.ModelMultipleChoiceField(queryset=Affiliate.objects.all(), required=False)
    setting = forms.MultipleChoiceField(choices=choices.SETTING, required=False)
    service_categories = forms.MultipleChoiceField(choices=choices.CORE_SERVICES, required=False)
    tiers_of_service = forms.MultipleChoiceField(choices=choices.TIERS_OF_SERVICE, required=False)
    tiers_of_evidence = forms.MultipleChoiceField(choices=choices.TIERS_OF_EVIDENCE, required=False)

    class Meta:
        model = Partner
        exclude = ['search_content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self.instance, 'pk'):
            self.fields['featured_network'].queryset = self.instance.network_use.all()
        else:
            self.fields['featured_network'].queryset = Affiliate.affiliates.none()


class PartnerSearchForm(SearchForm):
    """
    Form class for searching partners
    """
    grade = forms.MultipleChoiceField(choices=choices.GRADES, required=False)
    gender = forms.MultipleChoiceField(choices=choices.GENDER, required=False)
    reach = forms.MultipleChoiceField(required=False)
    need = forms.MultipleChoiceField(choices=choices.STUDENT_NEEDS, required=False)
    service_tiers = forms.MultipleChoiceField(choices=choices.TIERS_OF_SERVICE, required=False)
    setting = forms.MultipleChoiceField(choices=choices.SETTING, required=False)
    use_in_network = forms.BooleanField(required=False)
    service_categories = forms.MultipleChoiceField(required=False)
    free_of_cost = forms.NullBooleanField(required=False)
    evidence_tiers = forms.MultipleChoiceField(choices=choices.TIERS_OF_EVIDENCE, required=False)
