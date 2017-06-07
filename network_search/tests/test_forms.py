from network_search.core.forms import SearchForm


def test_query_in_search_form():
    form = SearchForm({'q': 'Hello'})
    assert form.is_valid()
    assert form.cleaned_data['q'] == 'Hello'


def test_blank_query_in_search_form():
    form = SearchForm({'q': ''})
    assert form.is_valid()
    assert form.cleaned_data['q'] == ''


def test_no_query_in_search_form():
    """
    SearchForm should force-add a query pararmter 'q'
    """
    form = SearchForm()
    assert form.is_valid()
    assert form.cleaned_data['q'] == ''
