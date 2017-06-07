from django import forms

from network_search.affiliates.models import Affiliate
from network_search.core.forms import SearchForm
from network_search.programs.models import Program

GRADE_CHOICES = [
    ('high school', 'High School'),
    ('middle school', 'Middle School'),
]


class ProgramAdminForm(forms.ModelForm):

    grade = forms.MultipleChoiceField(choices=GRADE_CHOICES, required=False)

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
