from django import forms

from network_search.core.models import Link


class SearchForm(forms.Form):
    q = forms.CharField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        data = data or {}
        if 'q' not in data:
            data['q'] = ''
        super().__init__(data=data, *args, **kwargs)


class RequiredLinkForm(forms.ModelForm):
    """
    This form class requires the URL field is filled out

    When used in the admin it results in the loss of the admin form's
    clickable link attribute, and so is not used.
    """
    url = forms.URLField(required=True)

    class Meta:
        fields = '__all__'
        model = Link
