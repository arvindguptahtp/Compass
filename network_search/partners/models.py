from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models
from model_utils.models import TimeStampedModel

from network_search.core.models import Link


class PartnerQueryset(models.QuerySet):

    def active(self):
        return self.filter(is_removed=False)

    def delete(self):
        self.update(is_removed=True)


class Partner(TimeStampedModel):
    """
    Represents a partner organization
    """
    is_removed = models.BooleanField(default=False)
    name = models.CharField(max_length=400)

    contact_name = models.CharField(max_length=100)
    contact_title = models.CharField(max_length=100)
    contact_email = models.EmailField()

    website = models.URLField()

    mission = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    grade = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    gender = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    organizational_reach = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    student_need = ArrayField(
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
    service_categories = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )
    tiers_of_ebp = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
    )

    is_cost_free = models.BooleanField(blank=True)
    cost_description = models.CharField(max_length=200, blank=True, null=True)

    is_core_partner = models.BooleanField(blank=True)

    network_use = models.ManyToManyField('affiliates.Affiliate', related_name='partners', blank=True)
    featured_network = models.ManyToManyField('affiliates.Affiliate', related_name='featured_partners', blank=True)

    search_content = SearchVectorField()

    partners = PartnerQueryset.as_manager()
    objects = partners

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        """Keep the search field updated"""
        self.search_content = SearchVector('name', 'mission', 'overview')
        super().save(*args, **kwargs)

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


class WebinarLink(Link):
    partner = models.ForeignKey('Partner', related_name='webinars')


class PresentationsLink(Link):
    partner = models.ForeignKey('Partner', related_name='presentations')
