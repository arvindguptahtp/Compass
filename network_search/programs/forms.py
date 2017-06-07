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
    network_use = forms.ModelMultipleChoiceField(
        queryset=Affiliate.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Program
        exclude = ['search_content']


class ProgramSearchForm(SearchForm):
    """
    Form class for searching programs
    """
