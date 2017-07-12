from django import forms

from network_search.core import choices
from network_search.affiliates import models
from network_search.core.forms import SearchForm
from network_search.core.choices import BudgetLevel

try:
    from s3direct.widgets import S3DirectWidget
except ImportError:
    widget = forms.FileInput()
else:
    widget = S3DirectWidget(dest='affiliate_imports')


class GradeLevel(choices.Choice):
    el = "Elementary (Pre-K - 5)"
    ms = "Middle School (6 - 8)"
    hs = "High School (9 -12)"


class ExcelUploadForm(forms.ModelForm):

    data_file = forms.FileField(widget=widget)

    class Meta:
        fields = '__all__'
        model = models.ExcelUpload


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
    gender = forms.MultipleChoiceField(
        choices=choices.Gender.as_choices(),
        required=False,
    )
    race = forms.MultipleChoiceField(
        choices=choices.Race.as_choices(),
        required=False,
    )
    served = forms.MultipleChoiceField(
        choices=choices.StudentCharacteristics.as_choices(),
        required=False,
    )
    location = forms.ChoiceField(
        choices=choices.AffiliateLocation.as_choices(),
        required=False,
    )
    budget = forms.ChoiceField(
        choices=BudgetLevel.as_choices(),
        required=False,
    )

    # Service provision search
    academic_assistance = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    basic_needs = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    behavior_intervention = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    college_career_prep = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    comm_service = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    enrichment = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    family_engagement = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    life_skills = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    physical_fitness_health = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )
    prof_mental_health = forms.ChoiceField(
        choices=choices.ServiceProvision.as_choices(),
        required=False,
    )

    # Staffing search
    staff_pt = forms.BooleanField(required=False)
    staff_ft = forms.BooleanField(required=False)
    staff_ac = forms.BooleanField(required=False)
