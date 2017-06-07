from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        data = data or {}
        if 'q' not in data:
            data['q'] = ''
        super().__init__(data=data, *args, **kwargs)
