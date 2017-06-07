"""
Models for the affiliate directory and EOY data reports
"""

from django.db import models
from model_utils.models import TimeStampedModel

from network_search.core.models import Link, BaseResource, ResourceQueryset


class AffiliateQueryset(ResourceQueryset):
    def search(self, **kwargs):
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


class EndOfYear(TimeStampedModel):
    is_active = models.BooleanField(blank=True)
    year_ends = models.IntegerField(help_text="This is the calendar year in which the EOY data ends. "
                                    "E.g. for the 2019-2020 year enter '2020'.")

    def __str__(self):
        return "{}-{}".format(self.year_ends - 1, self.year_ends)

    def save(self, **kwargs):
        """Ensures no other EOY values are active on save"""
        if self.is_active:
            self.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(**kwargs)
