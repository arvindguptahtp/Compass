from django.db import models
from django.contrib.postgres.fields import ArrayField

from network_search.core.models import Link
from network_search.core.models import BaseResource
from network_search.core.models import ResourceQueryset


class PartnerQueryset(ResourceQueryset):
    def search(self, **kwargs):
        qs = super().search(**kwargs)

        grades = kwargs.pop('grade', [])
        genders = kwargs.pop('gender', [])
        needs = kwargs.pop('need', [])

        if grades:
            qs = qs.filter(grade__contains=grades)
        if genders:
            qs = qs.filter(gender__contains=genders)
        if needs:
            qs = qs.filter(student_need__contains=needs)

        return qs


class Partner(BaseResource):
    """
    Represents a partner organization
    """

    url_name = "partner_detail"
    search_content_fields = ['name', 'mission', 'overview']

    contact_name = models.CharField(max_length=100)
    contact_title = models.CharField(max_length=100)
    contact_email = models.EmailField()

    website = models.URLField()

    mission = models.TextField(blank=True)
    overview = models.TextField(blank=True)

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
    organizational_reach = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    student_need = ArrayField(
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
    service_categories = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )
    tiers_of_evidence = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )

    is_cost_free = models.BooleanField(blank=True, default=False)
    cost_description = models.CharField(max_length=200, blank=True, null=True)

    is_core_partner = models.BooleanField(blank=True, default=False)  # is this based on link from Program???

    network_use = models.ManyToManyField('affiliates.Affiliate', related_name='partners', blank=True)
    featured_network = models.ManyToManyField('affiliates.Affiliate', related_name='featured_partners', blank=True)

    partners = PartnerQueryset.as_manager()
    objects = partners


class WebinarLink(Link):
    partner = models.ForeignKey('Partner', related_name='webinars')


class PresentationsLink(Link):
    partner = models.ForeignKey('Partner', related_name='presentations')
