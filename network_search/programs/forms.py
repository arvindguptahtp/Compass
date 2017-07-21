from django import forms

from network_search.core import choices
from network_search.core.forms import SearchForm
from network_search.programs.models import Program


class ProgramAdminForm(forms.ModelForm):

    grade = forms.MultipleChoiceField(
        choices=choices.ProgramGrades.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    gender = forms.MultipleChoiceField(
        choices=choices.Gender.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    race = forms.MultipleChoiceField(
        choices=choices.Race.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    region = forms.MultipleChoiceField(
        choices=choices.Regions.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    student_need = forms.MultipleChoiceField(
        choices=choices.StudentNeeds.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    student_characteristics = forms.MultipleChoiceField(
        choices=choices.StudentCharacteristics.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    setting = forms.MultipleChoiceField(
        choices=choices.Setting.as_choices(),
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
    service_categories = forms.MultipleChoiceField(
        choices=choices.CoreServices.as_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    is_cost_free = forms.BooleanField(
        required=False,
        label="Is cost free?",
    )
    assessment_available = forms.BooleanField(
        required=False,
        label="Assessment available?",
    )

    class Meta:
        model = Program
        exclude = ['search_content']


class ProgramSearchForm(SearchForm):
    """
    Form class for searching programs
    """
    grade = forms.MultipleChoiceField(
        choices=choices.ProgramGrades.as_choices(),
        required=False,
    )
    gender = forms.MultipleChoiceField(
        choices=choices.Gender.as_choices(),
        required=False,
    )
    race = forms.MultipleChoiceField(
        choices=choices.Race.as_choices(),
        required=False,
    )
    need = forms.MultipleChoiceField(
        choices=choices.StudentNeeds.as_choices(),
        required=False,
    )
    service_tiers = forms.MultipleChoiceField(
        choices=choices.TiersOfService.as_choices(),
        required=False,
    )
    use_in_network = forms.NullBooleanField(
        required=False,
    )
    services = forms.MultipleChoiceField(
        label="Service Categories",
        choices=choices.CoreServices.as_choices(),
        required=False,
    )
    free_of_cost = forms.NullBooleanField(required=False)
    evidence = forms.MultipleChoiceField(
        label="Tiers of Evidence",
        choices=choices.TiersOfEvidence.as_choices(),
        required=False,
    )
