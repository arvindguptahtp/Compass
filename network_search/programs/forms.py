from django import forms

from network_search.core import choices
from network_search.core.forms import SearchForm
from network_search.programs.models import Program


class ProgramAdminForm(forms.ModelForm):

    grade = forms.MultipleChoiceField(choices=choices.Grades.as_choices(), required=False)
    gender = forms.MultipleChoiceField(choices=choices.Gender.as_choices(), required=False)
    race = forms.MultipleChoiceField(choices=choices.Race, required=False)
    region = forms.MultipleChoiceField(choices=choices.Regions.as_choices(), required=False)
    student_need = forms.MultipleChoiceField(choices=choices.StudentNeeds.as_choices(), required=False)
    student_characteristics = forms.MultipleChoiceField(choices=choices.STUDENT_CHARACTERISTICS, required=False)
    setting = forms.MultipleChoiceField(choices=choices.SETTING, required=False)
    tiers_of_service = forms.MultipleChoiceField(choices=choices.TIERS_OF_SERVICE, required=False)
    tiers_of_evidence = forms.MultipleChoiceField(choices=choices.TIERS_OF_EVIDENCE, required=False)
    service_categories = forms.MultipleChoiceField(choices=choices.CORE_SERVICES, required=False)

    class Meta:
        model = Program
        exclude = ['search_content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['featured_network'].queryset = self.instance.network_use.all()


class ProgramSearchForm(SearchForm):
    """
    Form class for searching programs
    """
