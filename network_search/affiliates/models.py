"""
Models for the affiliate directory and EOY data reports
"""

import logging

from django.db import models
from django.db.models import F
from django.db.models import Sum
from model_utils.models import TimeStampedModel
from django.utils.functional import cached_property
from django.contrib.postgres.fields import ArrayField

from network_search.core import choices
from network_search.core.models import DataUpload
from network_search.core.models import BaseResource
from network_search.core.models import ResourceQueryset

logger = logging.getLogger(__name__)

# Used to simplify and remove literals for fields in school data
female_template = "students_female_{}"
male_template = "students_male_{}"
gender_templates = [female_template, male_template]


class EOYQueryset(models.QuerySet):
    def current(self) -> models.Model:
        """Returns the latest published report year"""
        return self.filter(is_active=True).order_by('-year_ends').first()


class AffiliateQueryset(ResourceQueryset):
    def search(self, **kwargs) -> models.QuerySet:
        qs = super().search(**kwargs)

        eoy = EndOfYear.years.current()
        if eoy is None:
            logger.error("Attempting to search affiliates without an active reporting year")
            return qs

        logger.debug("Searching affiliates using {}".format(eoy))
        qs = qs.filter(affiliate_eoy_data__year=eoy)

        genders = kwargs.pop('gender', [])
        race = kwargs.pop('race', [])

        if genders:
            qs = qs.filter(
                affiliate_eoy_data__search_gender__contains=genders,
                affiliate_eoy_data__year=eoy,
            )
        if race:
            qs = qs.filter(
                affiliate_eoy_data__search_race__contains=race,
                affiliate_eoy_data__year=eoy,
            )

        return qs.filter(affiliate_eoy_data__year=eoy).distinct()


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
    address_state = models.CharField(max_length=30)
    address_postcode = models.CharField(max_length=10)
    shipping_address = models.CharField(max_length=400, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True)
    fax_number = models.CharField(max_length=30, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    affiliate_location = models.CharField(max_length=3)

    affiliates = AffiliateQueryset.as_manager()
    objects = affiliates
    default_manager = models.Manager()

    class Meta:
        verbose_name = "Affiliate"
        verbose_name_plural = "Affiliates"

    def current_data(self):
        return self.affiliate_eoy_data.filter(year=EndOfYear.years.current()).first()


class AffiliateEOYData(TimeStampedModel):
    affiliate = models.ForeignKey('Affiliate', related_name='affiliate_eoy_data')
    year = models.ForeignKey('EndOfYear', related_name='affiliate_eoy_data')

    districts = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        help_text="School district names should be separated by commas.",
    )

    executive_director_name = models.CharField(null=True, max_length=200)
    executive_director_email = models.EmailField(null=True, max_length=200)
    program_lead_name = models.CharField(null=True, max_length=200)
    program_lead_email = models.EmailField(null=True, max_length=200)

    budget_total = models.IntegerField(default=0)

    staff_fulltime_affiliate = models.IntegerField(default=0)
    staff_parttime_affiliate = models.IntegerField(default=0)
    staff_fulltime_non_affiliate = models.IntegerField(default=0)
    staff_parttime_non_affiliate = models.IntegerField(default=0)
    staff_fulltime_americorps = models.IntegerField(default=0)
    staff_parttime_americorps = models.IntegerField(default=0)

    search_students_female = models.IntegerField(default=0, editable=False)
    search_students_male = models.IntegerField(default=0, editable=False)
    search_gender = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )

    search_students_american_indian = models.IntegerField(default=0, editable=False)
    search_students_asian = models.IntegerField(default=0, editable=False)
    search_students_black = models.IntegerField(default=0, editable=False)
    search_students_hispanic = models.IntegerField(default=0, editable=False)
    search_students_white = models.IntegerField(default=0, editable=False)
    search_students_two_or_more = models.IntegerField(default=0, editable=False)
    search_students_other = models.IntegerField(default=0, editable=False)
    search_race = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ('affiliate', 'year')
        verbose_name = "Affiliate EOY Data"
        verbose_name_plural = "Affiliate EOY Data"

    def __str__(self):
        return "{} ({})".format(self.affiliate.name, self.year)

    @property
    def school_districts_count(self):
        return len(self.school_districts)

    @cached_property
    def school_districts(self):
        return [i.strip() for i in self.districts.split(",")]

    def full_time_staff(self):
        return self.staff_fulltime_affiliate + self.staff_fulltime_non_affiliate

    def part_time_staff(self):
        return self.staff_parttime_affiliate + self.staff_parttime_non_affiliate

    def americorps_staff(self):
        return self.staff_parttime_americorps + self.staff_fulltime_americorps

    def calculate(self):
        self.search_students_female = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.female_fields]))
        )['total']
        self.search_students_male = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.male_fields]))
        )['total']

        self.search_gender = [e for e in [
            choices.Gender.f.name if self.search_students_female else None,
            choices.Gender.m.name if self.search_students_male else None,
        ] if e is not None]

        self.search_students_american_indian = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.american_indian_fields]))
        )['total']
        self.search_students_asian = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.asian_fields]))
        )['total']
        self.search_students_black = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.black_fields]))
        )['total']
        self.search_students_hispanic = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.hispanic_fields]))
        )['total']
        self.search_students_white = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.white_fields]))
        )['total']
        self.search_students_two_or_more = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.two_or_more_races_fields]))
        )['total']
        self.search_students_other = self.school_data.aggregate(
            total=Sum(sum([F(field) for field in SchoolEOYData.other_fields]))
        )['total']

        self.search_race = [e for e in [
            choices.Race.am.name if self.search_students_american_indian else None,
            choices.Race.asn.name if self.search_students_asian else None,
            choices.Race.bl.name if self.search_students_black else None,
            choices.Race.his.name if self.search_students_hispanic else None,
            choices.Race.wh.name if self.search_students_white else None,
            choices.Race.two.name if self.search_students_two_or_more else None,
        ] if e is not None]

        self.save()


class SchoolEOYData(TimeStampedModel):
    """
    School and Student affiliate data
    """

    female_fields = [
        female_template.format(race)
        for race in ['american_indian', 'asian', 'black', 'hispanic', 'white', 'two_or_more_races', 'other']
    ]
    male_fields = [
        male_template.format(race)
        for race in ['american_indian', 'asian', 'black', 'hispanic', 'white', 'two_or_more_races', 'other']
    ]

    american_indian_fields = [template.format(choices.Race.am.lower()) for template in gender_templates]
    asian_fields = [template.format(choices.Race.asn.lower()) for template in gender_templates]
    black_fields = [template.format(choices.Race.bl.lower()) for template in gender_templates]
    hispanic_fields = [template.format(choices.Race.his.lower()) for template in gender_templates]
    white_fields = [template.format(choices.Race.wh.lower()) for template in gender_templates]
    two_or_more_races_fields = [template.format(choices.Race.two.lower()) for template in gender_templates]
    other_fields = [template.format('other') for template in gender_templates]

    class Meta:
        verbose_name = "School and Student EOY Data"
        verbose_name_plural = "School and Student EOY Data"

    affiliate_data = models.ForeignKey('AffiliateEOYData', related_name='school_data')
    name = models.CharField(max_length=400)

    site_type = models.CharField(max_length=100, blank=True, null=True, choices=choices.AffiliateGrades.as_choices())
    location = models.CharField(max_length=100, blank=True, null=True)
    location_model = models.CharField(max_length=100, null=True)
    student_enrollment = models.IntegerField(default=0)

    service_academic_assistance = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_basic_needs = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_behavior_intervention = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_college_career_prep = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_comm_service = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_enrichment = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_family_engagement = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_life_skills = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_physical_fitness_health = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)
    service_prof_mental_health = models.CharField(
        null=True, choices=choices.ServiceProvision.as_choices(), max_length=100)

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
    students_k_11_ged = models.IntegerField(default=0)
    students_k_11_expelled = models.IntegerField(default=0)
    students_k_11_incarcerated = models.IntegerField(default=0)
    students_k_11_deceased = models.IntegerField(default=0)
    students_k_11_other = models.IntegerField(default=0)
    students_k_11_unknown = models.IntegerField(default=0)
    students_grade_12_graduated = models.IntegerField(default=0)
    students_grade_12_retained = models.IntegerField(default=0)
    students_grade_12_dropped_out = models.IntegerField(default=0)
    students_grade_12_transferred = models.IntegerField(default=0)
    students_grade_12_ged = models.IntegerField(default=0)
    students_grade_12_expelled = models.IntegerField(default=0)
    students_grade_12_incarcerated = models.IntegerField(default=0)
    students_grade_12_deceased = models.IntegerField(default=0)
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
        return "{}, {}".format(self.name, self.affiliate_data)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.affiliate_data.calculate()


class ExcelUpload(DataUpload):
    """
    Concrete model for affiliate data uploads
    """
    year = models.ForeignKey('EndOfYear', related_name="excel_uploads")

    def save(self, **kwargs):
        created = not bool(getattr(self, 'pk'))
        super().save(**kwargs)
        if created:
            from network_search.affiliates.tasks import process_data_upload
            process_data_upload.delay(self.pk)
