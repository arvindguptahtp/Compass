from django import forms

from network_search.core.models import Link
from network_search.affiliates.models import Affiliate


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


class FeaturedMixin:
    """Filter featured affiliates"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self.instance, 'pk'):
            self.fields['featured_network'].queryset = self.instance.network_use.all()
        else:
            self.fields['featured_network'].queryset = Affiliate.affiliates.none()


class AnySelect(forms.NullBooleanSelect):
    """
    Replaces 'Unknown' with 'Any' in selection options
    """

    def __init__(self, attrs=None):
        choices = (
            ('1', 'Any'),
            ('2', 'Yes'),
            ('3', 'No'),
        )
        super(forms.Select, self).__init__(attrs, choices)
