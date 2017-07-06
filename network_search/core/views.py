from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView
from django.views.generic import TemplateView
from easy_pdf.views import PDFTemplateResponseMixin
from pure_pagination import PageNotAnInteger
from pure_pagination import Paginator
from django.conf import settings


class HomePage(TemplateView):
    """The home page view"""
    template_name = "site/index.html"


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

        Works with GET or POST
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        request_dict = self.request.GET.copy() if self.request.method == 'GET' else self.request.POST.copy()
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
