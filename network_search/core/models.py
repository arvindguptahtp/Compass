from django.db import models
from model_utils.models import TimeStampedModel
from django.core.urlresolvers import reverse
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchVectorField


class Link(TimeStampedModel):
    """
    A model for links with optional titles

    The `url` field is nullable so that the title may be used without a link,
    allowing not just lists of links but lists of described resources with or
    without links as may be avaialble.
    """

    title = models.CharField(max_length=100, blank=True, null=True, help_text="Optional visible for link")
    url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

    @property
    def label(self):
        """Returns a label appropriate for displaying on the front end"""
        return self.title if self.title else self.url


class BaseResource(TimeStampedModel):
    is_removed = models.BooleanField(default=False)
    name = models.CharField(max_length=400)
    search_content = SearchVectorField()

    search_content_fields = []
    url_name = ""

    class Meta:
        abstract = True

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        """Keep the search field updated

        This uses F expressions under the hood so the values must first be save
        """
        super().save(*args, **kwargs)
        self.search_content = SearchVector(*self.search_content_fields)
        kwargs.update({'force_insert': False})
        super().save(update_fields=['search_content'], *args, **kwargs)

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_removed = True
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)

    def get_absolute_url(self):
        return reverse(self.url_name, kwargs={"pk": self.pk})


class ResourceQueryset(models.QuerySet):
    """
    Common queryset interface
    """

    def active(self) -> models.QuerySet:
        return self.filter(is_removed=False)

    def delete(self) -> None:
        self.update(is_removed=True)

    def search(self, **kwargs) -> models.QuerySet:
        """
        Returns a queryset by filtering from a search form's cleaned data

        The keyword arguments are not expected to be [queryset] filter ready
        but instead to need checking and then transformation.

        Args:
            **kwargs: the search form's cleaned data

        Returns:
            Searched/filtered queryset

        """
        qs = self.all()
        query = kwargs.pop('q', '')
        if query:
            qs = qs.filter(search_content=query)

        return qs
