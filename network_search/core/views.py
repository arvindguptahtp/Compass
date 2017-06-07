from django.views.generic import FormView
from pure_pagination import Paginator, PageNotAnInteger
from django.core.exceptions import ImproperlyConfigured


class SearchView(FormView):
    """
    List and search 
    
    Attributes:
        queryset: the queryset to list and filter
        form_class: the form class for 
        template_name: path to the template
        context_object_name: string name of the paging object
    """
    queryset = None
    context_object_name = "paginator"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.queryset is None:
            raise ImproperlyConfigured("You must define a 'queryset' attribute on the view class")

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.

        Customized here to ensure that the optional 'q' is always included,
        thus ensuring that the form *always* gets at least one input. Otherwise
        if the form is initialized with an empty dict it will be invalid.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        request_dict = self.request.GET.copy() if self.request.method == 'GET' else self.request.POST.copy()

        if 'q' not in request_dict:
            request_dict.update({'q': ''})

        kwargs.update({'data': request_dict})

        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            queryset = self.queryset.search(**form.cleaned_data)
        else:
            queryset = self.queryset

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(queryset, request=request, per_page=20)
        paged_queryset = p.page(page)

        return self.render_to_response(self.get_context_data(**{
            'form': form,
            self.context_object_name: paged_queryset,
        }))
