"""
Models for the affiliate directory and EOY data reports

Fields namespaced with `search_` are aggregate fields.
"""

import logging
from functools import reduce
from typing import Optional

from django.db import models
from django.db.models import F
from django.db.models import Q
from django.db.models import Sum
from model_utils.models import TimeStampedModel
from django.utils.functional import cached_property
from django.contrib.postgres.fields import ArrayField

from network_search.core import choices
from network_search.core.models import DataUpload
from network_search.core.models import BaseResource
from network_search.core.models import ResourceQueryset
from network_search.core.templatetags.network_search_tags import us_state

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
        """
        Returns a queryset based on a search form's cleaned data

        The seemingly redundant filtering against the current EndOfYear reporting
        year below ensures that each step excludes undesired data which otherwise
        has been included.
        """
        qs = super().search(**kwargs)

        service_field_names = [
            'academic_assistance', 'basic_needs', 'behavior_intervention',
            'college_career_prep', 'comm_service', 'enrichment', 'family_engagement',
            'life_skills', 'physical_fitness_health', 'prof_mental_health'
        ]
        staff_fields = {
            'ft': ['staff_fulltime_affiliate', 'staff_fulltime_non_affiliate'],
            'pt': ['staff_parttime_affiliate', 'staff_parttime_non_affiliate'],
            'ac': ['staff_parttime_americorps', 'staff_fulltime_americorps'],
        }
        grade_fields = {
            choices.GradeLevel.el.name: [
                'students_grade_prek',
                'students_grade_k',
                'students_grade_1',
                'students_grade_2',
                'students_grade_3',
                'students_grade_4',
                'students_grade_5',
            ],
            choices.GradeLevel.ms.name: [
                'students_grade_6',
                'students_grade_7',
                'students_grade_8',
            ],
            choices.GradeLevel.hs.name: [
                'students_grade_9',
                'students_grade_10',
                'students_grade_11',
                'students_grade_12',
            ],
        }

        eoy = EndOfYear.years.current()
        if eoy is None:
            logger.error("Attempting to search affiliates without an active reporting year")
            return qs.distinct('name')

        logger.debug("Searching affiliates using {}".format(eoy))
        qs = qs.filter(affiliate_eoy_data__year=eoy)

        genders = kwargs.pop('gender', [])
        race = kwargs.pop('race', [])
        served = kwargs.pop('served', [])
        location = kwargs.pop('location', None)
        budget = kwargs.pop('budget', None)
        grades = kwargs.pop('grades', [])
        staff = kwargs.pop('staff', [])

        if location:
            qs = qs.filter(affiliate_location=location)

        if budget == choices.BudgetLevel.zero_five.name:
            qs = qs.filter(
                affiliate_eoy_data__budget_total__lte=500000,
                affiliate_eoy_data__year=eoy,
            )
        elif budget == choices.BudgetLevel.five_one.name:
            qs = qs.filter(
                affiliate_eoy_data__budget_total__gt=500000,
                affiliate_eoy_data__budget_total__lte=1000000,
                affiliate_eoy_data__year=eoy,
            )
        elif budget == choices.BudgetLevel.one.name:
            qs = qs.filter(
                affiliate_eoy_data__budget_total__gt=1000000,
                affiliate_eoy_data__year=eoy,
            )

        if genders:
            qs = qs.filter(
                affiliate_eoy_data__search_gender__overlap=genders,
                affiliate_eoy_data__year=eoy,
            )
        if race:
            qs = qs.filter(
                affiliate_eoy_data__search_race__overlap=race,
                affiliate_eoy_data__year=eoy,
            )
        if served:
            qs = qs.filter(
                affiliate_eoy_data__search_served__overlap=served,
                affiliate_eoy_data__year=eoy,
            )

        filtered_fields = []
        for grade in grades:
            db_fields = grade_fields[grade]
            filter_field = 'grade_level_{}'.format(grade)
            filtered_fields.append(filter_field)
            qs = qs.filter(
                affiliate_eoy_data__year=eoy,
            ).annotate(
                **{filter_field: sum([F('affiliate_eoy_data__school_data__{}'.format(field)) for field in db_fields])}
            )
        grades_query = reduce(lambda q, value: q | Q(**{'{}__gt'.format(value): 0}), filtered_fields, Q())
        qs = qs.filter(grades_query)

        for staff_level in staff:
            db_fields = staff_fields[staff_level]
            qs = qs.annotate(
                has_staff=sum([F("affiliate_eoy_data__{}".format(field)) for field in db_fields])
            ).filter(
                has_staff__gt=0,
                affiliate_eoy_data__year=eoy,
            )

        for service_name in service_field_names:
            service_level = kwargs.pop(service_name, None)
            if service_level:
                filter_kwargs = {
                    'affiliate_eoy_data__year': eoy,
                    'affiliate_eoy_data__school_data__service_{}'.format(service_name): service_level,
                }
                qs = qs.filter(**filter_kwargs)

        return qs.filter(affiliate_eoy_data__year=eoy).distinct('name')


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

    funding_public_federal = models.IntegerField(default=0)
    funding_public_state = models.IntegerField(default=0)
    funding_public_city = models.IntegerField(default=0)
    funding_public_school_district = models.IntegerField(default=0)

    funding_private_corporate = models.IntegerField(default=0)
    funding_private_foundation = models.IntegerField(default=0)
    funding_private_board = models.IntegerField(default=0)
    funding_private_individual = models.IntegerField(default=0)
    funding_private_events = models.IntegerField(default=0)
    funding_private_cis_national = models.IntegerField(default=0)
    funding_private_cis_state_office = models.IntegerField(default=0)
    funding_private_npo = models.IntegerField(default=0)
    funding_private_other = models.IntegerField(default=0)

    @cached_property
    def funding_public(self) -> int:
        return sum([
            self.funding_public_federal,
            self.funding_public_state,
            self.funding_public_city,
            self.funding_public_school_district,
        ])

    @cached_property
    def funding_private(self) -> int:
        return sum([
            self.funding_private_corporate,
            self.funding_private_foundation,
            self.funding_private_board,
            self.funding_private_individual,
            self.funding_private_events,
            self.funding_private_cis_national,
            self.funding_private_cis_state_office,
            self.funding_private_npo,
            self.funding_private_other,
        ])

    @cached_property
    def funding_total(self) -> int:
        return self.funding_public + self.funding_private

    @cached_property
    def funding_percent_private(self) -> int:
        return int(round((self.funding_private / self.funding_total) * 100, ndigits=0))

    @cached_property
    def funding_percent_public(self):
        return int(round((self.funding_public / self.funding_total) * 100, ndigits=0))

    total_enrollment = models.IntegerField(default=0, editable=False)

    # Tracks when affiliates have a school that works with students meeting characteristic
    search_served = ArrayField(
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
        try:
            return [i.strip() for i in self.districts.split(",")]
        except AttributeError:
            return ""

    def calculated_total_case_managed(self):
        return self._sum_child_fields('students_case_managed')

    def calculated_total_students_reached(self):
        return self._sum_child_fields('students_total')

    def full_time_staff(self):
        return self.staff_fulltime_affiliate + self.staff_fulltime_non_affiliate

    def part_time_staff(self):
        return self.staff_parttime_affiliate + self.staff_parttime_non_affiliate

    def americorps_staff(self):
        return self.staff_parttime_americorps + self.staff_fulltime_americorps

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

    def _sum_child_fields(self, *fields):
        return self.school_data.aggregate(
            total=Sum(sum([F(field) for field in fields]))
        )['total']

    def calculated_total_enrollment(self):
        return self._sum_child_fields('student_enrollment')

    def total_students_incarcerated_parent(self):
        return self._sum_child_fields('students_served_incarcerated_parent')

    def total_students_gang(self):
        return self._sum_child_fields('students_served_gang')

    def total_students_child_of_military(self):
        return self._sum_child_fields('students_served_child_of_military')

    def total_students_adjudicated_youth(self):
        return self._sum_child_fields('students_served_adjudicated_youth')

    def total_students_substance_abuse(self):
        return self._sum_child_fields('students_served_substance_abuse')

    def total_students_special_education(self):
        return self._sum_child_fields('students_served_special_education')

    def total_students_pregnant_parenting(self):
        return self._sum_child_fields('students_served_pregnant_parenting')

    def total_students_lgbt(self):
        return self._sum_child_fields('students_served_lgbt')

    def total_students_homeless(self):
        return self._sum_child_fields('students_served_homeless')

    def total_students_foster(self):
        return self._sum_child_fields('students_served_foster')

    def total_students_ell(self):
        return self._sum_child_fields('students_served_ell')

    def total_students_frpl(self):
        return self._sum_child_fields('students_served_frpl')

    def total_students_served(self):
        return self._sum_child_fields('students_total')

    def students_k_11_promoted(self):
        return self._sum_child_fields('students_k_11_promoted')

    def students_k_11_retained(self):
        return self._sum_child_fields('students_k_11_retained')

    def students_k_11_dropped_out(self):
        return self._sum_child_fields('students_k_11_dropped_out')

    def students_k_11_transferred(self):
        return self._sum_child_fields('students_k_11_transferred')

    def students_k_11_ged(self):
        return self._sum_child_fields('students_k_11_ged')

    def students_k_11_expelled(self):
        return self._sum_child_fields('students_k_11_expelled')

    def students_k_11_incarcerated(self):
        return self._sum_child_fields('students_k_11_incarcerated')

    def students_k_11_deceased(self):
        return self._sum_child_fields('students_k_11_deceased')

    def students_k_11_other(self):
        return self._sum_child_fields('students_k_11_other')

    def students_k_11_unknown(self):
        return self._sum_child_fields('students_k_11_unknown')

    def students_grade_12_graduated(self):
        return self._sum_child_fields('students_grade_12_graduated')

    def students_grade_12_retained(self):
        return self._sum_child_fields('students_grade_12_retained')

    def students_grade_12_dropped_out(self):
        return self._sum_child_fields('students_grade_12_dropped_out')

    def students_grade_12_transferred(self):
        return self._sum_child_fields('students_grade_12_transferred')

    def students_grade_12_ged(self):
        return self._sum_child_fields('students_grade_12_ged')

    def students_grade_12_expelled(self):
        return self._sum_child_fields('students_grade_12_expelled')

    def students_grade_12_incarcerated(self):
        return self._sum_child_fields('students_grade_12_incarcerated')

    def students_grade_12_deceased(self):
        return self._sum_child_fields('students_grade_12_deceased')

    def students_grade_12_other(self):
        return self._sum_child_fields('students_grade_12_other')

    def students_grade_12_unknown(self):
        return self._sum_child_fields('students_grade_12_unknown')

    def calculate(self):
        """
        Aggregates school data and sets numeric and choice fields on the instance
        """

        self.total_enrollment = self._sum_child_fields('student_enrollment')

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

        self.search_served = [e for e in [
            choices.StudentCharacteristics.frpl.name if self.total_students_frpl() else None,
            choices.StudentCharacteristics.ay.name if self.total_students_adjudicated_youth() else None,
            choices.StudentCharacteristics.mil.name if self.total_students_child_of_military() else None,
            choices.StudentCharacteristics.ell.name if self.total_students_ell() else None,
            choices.StudentCharacteristics.fos.name if self.total_students_foster() else None,
            choices.StudentCharacteristics.gang.name if self.total_students_gang() else None,
            choices.StudentCharacteristics.hl.name if self.total_students_homeless() else None,
            choices.StudentCharacteristics.ip.name if self.total_students_incarcerated_parent() else None,
            choices.StudentCharacteristics.lgbt.name if self.total_students_lgbt() else None,
            choices.StudentCharacteristics.pp.name if self.total_students_pregnant_parenting() else None,
            choices.StudentCharacteristics.se.name if self.total_students_special_education() else None,
            choices.StudentCharacteristics.sa.name if self.total_students_substance_abuse() else None,
        ] if e is not None]

        self.save()

    def budget_as_range(self) -> str:
        """
        Returns a description of the total budget as a descriptive range

        E.g. '500k-1M'
        """
        if self.budget_total <= 500000:
            return choices.BudgetLevel.zero_five.value
        elif self.budget_total <= 1000000:
            return choices.BudgetLevel.five_one.value
        else:
            return choices.BudgetLevel.one.value


class Affiliate(BaseResource):
    """
    Represents the steady data for an affiliates directory

    All EOY data is related to this model
    """
    url_name = "affiliate_detail"
    search_content_fields = ["name", "official_name", "full_state_name"]

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
    affiliate_location = models.CharField(
        max_length=3,
        choices=choices.AffiliateLocation.as_choices(),
    )
    full_state_name = models.CharField(max_length=100, null=True, editable=False)

    affiliates = AffiliateQueryset.as_manager()
    objects = affiliates
    default_manager = models.Manager()

    class Meta(BaseResource.Meta):
        verbose_name = "Affiliate"
        verbose_name_plural = "Affiliates"

    def current_data(self) -> Optional[AffiliateEOYData]:
        """
        Get the affiliate data for the latest published reporting year
        """
        return self.affiliate_eoy_data.filter(year=EndOfYear.years.current()).first()

    def save(self, **kwargs):
        self.full_state_name = us_state(self.state)
        super().save(**kwargs)


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

    students_grade_prek = models.IntegerField(default=0)
    students_grade_k = models.IntegerField(default=0)
    students_grade_1 = models.IntegerField(default=0)
    students_grade_2 = models.IntegerField(default=0)
    students_grade_3 = models.IntegerField(default=0)
    students_grade_4 = models.IntegerField(default=0)
    students_grade_5 = models.IntegerField(default=0)
    students_grade_6 = models.IntegerField(default=0)
    students_grade_7 = models.IntegerField(default=0)
    students_grade_8 = models.IntegerField(default=0)
    students_grade_9 = models.IntegerField(default=0)
    students_grade_10 = models.IntegerField(default=0)
    students_grade_11 = models.IntegerField(default=0)
    students_grade_12 = models.IntegerField(default=0)

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

    partners = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "School and Student EOY Data"
        verbose_name_plural = "School and Student EOY Data"

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

    def copy(self):
        return ExcelUpload.objects.create(year=self.year, data_file=self.data_file)
