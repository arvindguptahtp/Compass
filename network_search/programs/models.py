from collections import OrderedDict

from django.contrib.postgres.fields import ArrayField
from django.db import models

from network_search.core.choices import TiersOfEvidence
from network_search.core.models import BaseResource
from network_search.core.models import Link
from network_search.core.models import ResourceQueryset

tier_levels = OrderedDict([
    (TiersOfEvidence.t1, 5),
    (TiersOfEvidence.t2, 4),
    (TiersOfEvidence.t3, 3),
    (TiersOfEvidence.t4, 2),
    (TiersOfEvidence.t5, 1),
])


class ProgramQueryset(ResourceQueryset):
    def search(self, **kwargs):
        qs = super().search(**kwargs)

        grades = kwargs.pop('grade', [])
        genders = kwargs.pop('gender', [])
        race = kwargs.pop('race', [])
        needs = kwargs.pop('need', [])
        service_tiers = kwargs.pop('service_tiers', [])
        services = kwargs.pop('services', [])
        evidence = kwargs.pop('evidence', [])
        cost_free = kwargs.pop('free_of_cost', None)
        use_in_network = kwargs.pop('use_in_network', None)

        if grades:
            qs = qs.filter(grade__contains=grades)
        if genders:
            qs = qs.filter(gender__contains=genders)
        if race:
            qs = qs.filter(race__contains=race)
        if needs:
            qs = qs.filter(student_need__contains=needs)
        if service_tiers:
            qs = qs.filter(tiers_of_service__contains=service_tiers)
        if services:
            qs = qs.filter(service_categories__contains=services)
        if evidence:
            qs = qs.filter(tiers_of_evidence__contains=evidence)

        if cost_free is not None:
            qs = qs.filter(is_cost_free=cost_free)

        if use_in_network is True:
            qs = qs.exclude(network_use=None)
        elif use_in_network is False:
            qs = qs.filter(network_use=None)

        return qs.distinct('name')

    def sorted(self, order_by: str = '') -> models.QuerySet:
        """Allows some non-standard sorting"""
        if order_by == 'evidence':
            return self.order_by('_tier_sorting')
        elif order_by == '-evidence':
            return self.order_by('-_tier_sorting')
        return self.order_by(order_by)


class Program(BaseResource):
    url_name = "program_detail"
    search_content_fields = ['name', 'summary', 'description']

    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)

    grade = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    gender = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    race = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    race_other = models.CharField(max_length=100, blank=True, null=True)
    region = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    region_other = models.CharField(max_length=100, blank=True, null=True)
    student_need = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    student_characteristics = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    tiers_of_service = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    setting = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    tiers_of_evidence = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    _tier_sorting = models.IntegerField(
        editable=False,
        null=True,
        default=0,
    )

    _study_details = models.TextField(name='study details', blank=True, null=True, help_text="Not for display")

    service_categories = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )

    assessment_available = models.BooleanField(default=False)
    assessment_info = models.CharField(max_length=400, blank=True, null=True)

    national_partner = models.ForeignKey('partners.Partner', blank=True, related_name="program", null=True)

    is_cost_free = models.BooleanField(blank=True, default=False)
    cost_description = models.CharField(max_length=200, blank=True, null=True)

    outcomes = models.TextField(blank=True, null=True)

    study_weblink = models.URLField(blank=True, null=True)
    program_weblink = models.URLField(blank=True, null=True)

    network_use = models.ManyToManyField('affiliates.Affiliate', related_name='programs', blank=True)
    featured_network = models.ManyToManyField(
        'affiliates.Affiliate',
        related_name='featured_programs',
        help_text="This is populated by first selecting affiliates for 'Network Use' and saving.",
        blank=True,
    )

    programs = ProgramQueryset.as_manager()
    objects = programs

    def save(self, *args, **kwargs):
        tiers = self.tiers_of_evidence or []
        for key, val in tier_levels.items():
            if key in tiers:
                self._tier_sorting = val
                break
        super().save(*args, **kwargs)

    def evidence_base(self):
        """Returns either the last evidence choice or ''
        """
        try:
            return self.tiers_of_evidence[-1]
        except TypeError:
            return ''


class NationalDatabase(Link):
    program = models.ForeignKey('Program', related_name="national_databases")


class AdditionalResource(Link):
    program = models.ForeignKey('Program', related_name="additional_resources")


class RelatedResource(Link):
    program = models.ForeignKey('Program', related_name="related_resources")
