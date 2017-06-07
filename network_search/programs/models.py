from django.contrib.postgres.fields import ArrayField
from django.db import models

from network_search.core.models import Link, BaseResource, ResourceQueryset


class ProgramQueryset(ResourceQueryset):
    def search(self, **kwargs):
        qs = super().search(**kwargs)
        return qs


class Program(BaseResource):
    url_name = "program_detail"
    search_content_fields = ['name']

    grade = ArrayField(
        models.CharField(max_length=100, blank=True),
    )

    network_use = models.ManyToManyField('affiliates.Affiliate', related_name='programs', blank=True)

    programs = ProgramQueryset.as_manager()
    objects = programs
