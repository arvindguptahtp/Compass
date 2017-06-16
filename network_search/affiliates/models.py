"""
Models for the affiliate directory and EOY data reports
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField
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


class Affiliate(BaseResource):
    """
    Represents the steady data for an affiliates directory

    All EOY data is related to this model
    """
    url_name = "affiliate_detail"
    search_content_fields = ["name", "official_name"]

    # Descriptive organizational info
    state = models.CharField(max_length=2)
    cis_id = models.IntegerField(verbose_name="Affiliate ID")
    official_name = models.CharField(max_length=200)
    address_street = models.CharField(max_length=200)
    address_city = models.CharField(max_length=200)
    address_state = models.CharField(max_length=2)
    address_postcode = models.CharField(max_length=10)
    shipping_address = models.CharField(max_length=400, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True)
    fax_number = models.CharField(max_length=30, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    affiliate_location = models.CharField(max_length=3)

    affiliates = AffiliateQueryset.as_manager()
    objects = affiliates

    class Meta:
        verbose_name = "Affiliate"
        verbose_name_plural = "Affiliates"


class AffiliateEOYData(TimeStampedModel):
    affiliate = models.ForeignKey('Affiliate', related_name='affiliate_eoy_data')
    year = models.ForeignKey('EndOfYear', related_name='affiliate_eoy_data')

    school_districts = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
        help_text="School district names should be separated by commas."
    )

    class Meta:
        unique_together = ('affiliate', 'year')
        verbose_name = "Affiliate EOY Data"
        verbose_name_plural = "Affiliate EOY Data"

    def __str__(self):
        return "{} ({})".format(self.affiliate.name, self.year)


class SchoolEOYData(TimeStampedModel):
    """
    School and Student affiliate data
    """

    class Meta:
        unique_together = ('affiliate', 'year')
        verbose_name = "School and Student EOY Data"
        verbose_name_plural = "School and Student EOY Data"

    affiliate = models.ForeignKey('Affiliate', related_name='school_eoy_data')

    year = models.ForeignKey('EndOfYear', related_name='school_eoy_data')
    name = models.CharField(verbose_name="school name", max_length=200)

    cis_model_school = models.BooleanField(default=False)

    service_categories = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )

    students_case_managed = models.IntegerField(default=0)
    students_total = models.IntegerField(default=0)

    students_female_american_indian = models.IntegerField(default=0)
    students_female_asian = models.IntegerField(default=0)
    students_female_black = models.IntegerField(default=0)
    students_female_hispanic = models.IntegerField(default=0)
    students_female_white = models.IntegerField(default=0)
    students_female_two_or_more_races = models.IntegerField(default=0)
    students_female_other = models.IntegerField(default=0)
    students_female_unknown = models.IntegerField(default=0)
    students_male_american_indian = models.IntegerField(default=0)
    students_male_asian = models.IntegerField(default=0)
    students_male_black = models.IntegerField(default=0)
    students_male_hispanic = models.IntegerField(default=0)
    students_male_white = models.IntegerField(default=0)
    students_male_two_or_more_races = models.IntegerField(default=0)
    students_male_other = models.IntegerField(default=0)
    students_male_unknown = models.IntegerField(default=0)
    students_unknown_race_gender = models.IntegerField(default=0)

    students_k_11_promoted = models.IntegerField(default=0)
    students_k_11_retained = models.IntegerField(default=0)
    students_k_11_dropped_out = models.IntegerField(default=0)
    students_k_11_transferred = models.IntegerField(default=0)
    students_k_11_other = models.IntegerField(default=0)
    students_k_11_unknown = models.IntegerField(default=0)
    students_grade_12_graduated = models.IntegerField(default=0)
    students_grade_12_retained = models.IntegerField(default=0)
    students_grade_12_dropped_out = models.IntegerField(default=0)
    students_grade_12_transferred = models.IntegerField(default=0)
    students_grade_12_other = models.IntegerField(default=0)
    students_grade_12_unknown = models.IntegerField(default=0)

    students_served_frpl = models.IntegerField(default=0)
    students_served_ell = models.IntegerField(default=0)
    students_served_foster = models.IntegerField(default=0)
    students_served_homeless = models.IntegerField(default=0)
    students_served_lgbt = models.IntegerField(default=0)
    students_served_pregnant_parenting = models.IntegerField(default=0)
    students_served_special_education = models.IntegerField(default=0)
    students_served_substance_abuse = models.IntegerField(default=0)
    students_served_adjudicated_youth = models.IntegerField(default=0)
    students_served_child_of_military = models.IntegerField(default=0)
    students_served_gang = models.IntegerField(default=0)
    students_served_incarcerated_parent = models.IntegerField(default=0)

    def __str__(self):
        return "{}, {} ({})".format(self.name, self.affiliate.name, self.year)
