"""
Models for the affiliate directory and EOY data reports
"""

from django.db import models

from model_utils.models import TimeStampedModel
from network_search.core.models import BaseResource
from network_search.core.models import ResourceQueryset


class EOYQueryset(models.QuerySet):
    def current(self) -> models.Model:
        """Returns the latest published report year"""
        return self.filter(is_active=True).order_by('-year').first()


class AffiliateQueryset(ResourceQueryset):
    def search(self, **kwargs) -> models.QuerySet:
        qs = super().search(**kwargs)
        return qs


class Affiliate(BaseResource):
    """
    Represents the steady data for an affiliates directory

    All EOY data is related to this model
    """
    url_name = "affiliate_detail"
    search_content_fields = ["name"]

    affiliates = AffiliateQueryset.as_manager()
    objects = affiliates

    class Meta:
        verbose_name = "Affiliate"
        verbose_name_plural = "Affiliates"


class EndOfYear(TimeStampedModel):
    is_active = models.BooleanField(blank=True)
    year_ends = models.IntegerField(
        unique=True,
        help_text="This is the calendar year in which the EOY data ends. E.g. for the 2019-2020 year enter '2020'.",
    )

    years = EOYQueryset.as_manager()
    objects = years

    class Meta:
        ordering = ['-year_ends']
        verbose_name = "Reporting Year"
        verbose_name_plural = "Reporting Years"

    def __str__(self):
        return "{}-{}".format(self.year_ends - 1, self.year_ends)

    def save(self, **kwargs):
        """Ensures no other EOY values are active on save"""
        if self.is_active:
            EndOfYear.years.exclude(pk=self.pk).update(is_active=False)
        super().save(**kwargs)


class AffiliateEOYData(TimeStampedModel):
    affiliate = models.ForeignKey('Affiliate', related_name='affiliate_eoy_data')
    year = models.ForeignKey('EndOfYear', related_name='affiliate_eoy_data')

    class Meta:
        unique_together = ('affiliate', 'year')
        verbose_name = "Affiliate EOY Data"
        verbose_name_plural = "Affiliate EOY Data"


class SchoolEOYData(TimeStampedModel):
    affiliate = models.ForeignKey('Affiliate', related_name='school_eoy_data')
    year = models.ForeignKey('EndOfYear', related_name='school_eoy_data')

    class Meta:
        unique_together = ('affiliate', 'year')
        verbose_name = "School EOY Data"
        verbose_name_plural = "School EOY Data"

class StudentEOYData(TimeStampedModel):
    affiliate = models.ForeignKey('Affiliate', related_name='student_eoy_data')
    year = models.ForeignKey('EndOfYear', related_name='student_eoy_data')

    class Meta:
        unique_together = ('affiliate', 'year')
        verbose_name = "Student EOY Data"
        verbose_name_plural = "Student EOY Data"
