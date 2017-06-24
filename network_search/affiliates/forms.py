from django import forms

from network_search.core import choices
from network_search.affiliates import models
from network_search.core.forms import SearchForm

try:
    from s3direct.widgets import S3DirectWidget
except ImportError:
    widget = forms.FileInput()
else:
    widget = S3DirectWidget(dest='affiliate_imports')


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
    gender = forms.MultipleChoiceField(choices=choices.Gender.as_choices(), required=False)
    race = forms.MultipleChoiceField(choices=choices.Race.as_choices(), required=False)
