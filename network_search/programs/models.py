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

    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)

    grade = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    gender = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    race = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    region = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    student_need = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    student_characteristics = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    tiers_of_service = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    setting = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    tiers_of_evidence = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )

    core_service_categories = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )

    assessment_available = models.BooleanField()
    assessment_info = models.CharField(max_length=400, blank=True, null=True)

    national_partner = models.ForeignKey('partners.Partner', blank=True, related_name="program", null=True)

    is_cost_free = models.BooleanField(blank=True)
    cost_description = models.CharField(max_length=200, blank=True, null=True)

    outcomes = models.TextField(blank=True)

    study_weblink = models.URLField(blank=True, null=True)

    network_use = models.ManyToManyField('affiliates.Affiliate', related_name='programs', blank=True)
    featured_network = models.ManyToManyField('affiliates.Affiliate', related_name='featured_programs', blank=True)

    programs = ProgramQueryset.as_manager()
    objects = programs


class NationalDatabase(Link):
    program = models.ForeignKey('Program', related_name="national_databases")


class RelatedResource(Link):
    program = models.ForeignKey('Program', related_name="related_resources")
