from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView
from django.views.generic import TemplateView
from easy_pdf.views import PDFTemplateResponseMixin
from pure_pagination import PageNotAnInteger
from pure_pagination import Paginator


class HomePage(TemplateView):
    """The home page view"""
    template_name = "pages/index.html"


class PDFMixin(PDFTemplateResponseMixin):
    def get_base_url(self):
        try:
            return settings.PDF_IMAGE_ROOT
        except AttributeError:
            return "{}://{}:{}".format(
                self.request.scheme,
                self.request.META['SERVER_NAME'],
                self.request.META['SERVER_PORT'],
            )


class SearchView(FormView):
    """
    List and search base view used by individual resources

    Includes in the context the form, the queryset, and a `few_results` boolean
    value which indicates whether the user performed an active search (hitting
    submit on a form) and got fewer than one whole page worth of results.

    Attributes:
        queryset: the queryset to list and filter
        form_class: the form class for
        template_name: path to the template
        context_object_name: string name of the paging object
        paginate_by: integer for number of objects to include per page
    """
    queryset = None
    context_object_name = "paginator"
    paginate_by = 20
    few_results_message = """Try adjusting the filter options to broaden your search."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.queryset is None:
            raise ImproperlyConfigured("You must define a 'queryset' attribute on the view class")

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.

        Works with GET or POST
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        request_dict = self.request.GET.copy() if self.request.method == 'GET' else self.request.POST.copy()
        kwargs.update({'data': request_dict})
        return kwargs

    def did_search(self) -> bool:
        request_dict = self.request.GET.copy() if self.request.method == 'GET' else self.request.POST.copy()
        for key in request_dict.keys():
            if request_dict.get(key, None):
                return True
        return False

    def get_queryset(self, form):
        if form.is_valid():
            return self.queryset.search(**form.cleaned_data)
        else:
            return self.queryset

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        queryset = self.get_queryset(form)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(queryset, request=request, per_page=self.paginate_by)
        paged_queryset = p.page(page)

        if p.count < self.paginate_by and self.did_search():
            few_results = True
        else:
            few_results = False

        return self.render_to_response(self.get_context_data(**{
            'few_results': few_results,
            'few_results_message': self.few_results_message,
            'form': form,
            self.context_object_name: paged_queryset,
        }))
