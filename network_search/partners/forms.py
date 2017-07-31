from django import forms

from network_search.core import choices
from network_search.core.forms import FeaturedMixin
from network_search.core.forms import SearchForm
from network_search.core.forms import AnySelect
from network_search.partners.models import Partner


class PartnerAdminForm(FeaturedMixin, forms.ModelForm):

    grade = forms.MultipleChoiceField(
        choices=choices.PartnerGrades.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    gender = forms.MultipleChoiceField(
        choices=choices.Gender.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    setting = forms.MultipleChoiceField(
        choices=choices.Setting.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    service_categories = forms.MultipleChoiceField(
        choices=choices.CoreServices.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    tiers_of_service = forms.MultipleChoiceField(
        choices=choices.TiersOfService.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    tiers_of_evidence = forms.MultipleChoiceField(
        choices=choices.TiersOfEvidence.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    organizational_reach = forms.MultipleChoiceField(
        choices=choices.Regions.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    student_need = forms.MultipleChoiceField(
        choices=choices.StudentNeeds.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Partner
        exclude = ['search_content']


class PartnerSearchForm(SearchForm):
    """
    Form class for searching partners
    """
    grade = forms.MultipleChoiceField(choices=choices.AffiliateGrades.as_choices(), required=False)
    gender = forms.MultipleChoiceField(choices=choices.Gender.as_choices(), required=False)
    reach = forms.MultipleChoiceField(choices=choices.Regions.as_choices(), required=False)
    need = forms.MultipleChoiceField(choices=choices.StudentNeeds.as_choices(), required=False)
    service_tiers = forms.MultipleChoiceField(choices=choices.TiersOfService.as_choices(), required=False)
    setting = forms.MultipleChoiceField(choices=choices.Setting.as_choices(), required=False)
    use_in_network = forms.NullBooleanField(
        required=False,
        widget=AnySelect,
    )
    services = forms.MultipleChoiceField(
        label="Service Categories",
        choices=choices.CoreServices.as_choices(),
        required=False,
    )
    free_of_cost = forms.NullBooleanField(
        required=False,
        widget=AnySelect,
    )
    evidence = forms.MultipleChoiceField(
        label="Tiers of Evidence",
        choices=choices.TiersOfEvidence.as_choices(),
        required=False,
    )
