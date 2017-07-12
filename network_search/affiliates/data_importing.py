"""
Functionality specific to importing affiliate data

These enumerated types map a model field name (the enum name) to
the column name (the enum value) in the spreadsheet data source.
"""

import logging
from enum import Enum
from typing import Any
from collections import namedtuple

import pandas as pd

# A MappingType associates both the column name from the spreadsheet and
# the expected Python type with the model (database) field name. The type
# is used to fill empty fields.
MappingType = namedtuple('MappingType', ['column_name', 'type'])

logger = logging.getLogger(__name__)


nan_map = {
    str: "",
    int: 0,
}


class PandasMapper(Enum):

    @classmethod
    def as_choices(cls):
        return [
            (child.name, child.value.column_name)
            for child in cls
        ]

    @classmethod
    def all_names(cls):
        return [child.name for child in cls]

    @classmethod
    def all_values(cls):
        return [child.value for child in cls]

    @classmethod
    def reversed(cls):
        return {i.value: i.name for i in cls}

    @classmethod
    def defaults(cls, data_row):
        return {
            i.name: data_row[i.value.column_name]
            for i in cls
        }

    @classmethod
    def fillna(cls, df):
        for column_name, column_type in cls.all_values():
            try:
                df[column_name].fillna(nan_map[column_type], inplace=True)
            except KeyError:
                print("No such key '{}' in {}".format(column_name, df.keys()))

    @classmethod
    def safe_update(cls, data_row: pd.Series, obj: Any):
        """
        for field_name, (column_name, column_type) in cls:
            try:
                setattr(obj, field_name, data_row[column_name])
            except BaseException:
                logger.error("Could not set '{}' from '{}' on '{}'".format(
                    data_row.get(column_name, 'MISSING'),
                    column_name,
                    obj,
                ))
        """
        for i in cls:
            try:
                setattr(obj, i.name, data_row[i.value.column_name])
            except BaseException:
                logger.error("Could not set '{}' from '{}' on '{}'".format(
                    data_row.get(i.value.column_name, 'MISSING'),
                    i.value.column_name,
                    obj,
                ))
        try:
            obj.save()
        except BaseException:
            logger.exception("Could not save '{}'".format(obj))


class AffiliateFields(PandasMapper):
    """Maps model fields to spreadsheet (and DataFrame) column names

    Does NOT include "name" as this is used for a primary lookup
    """
    state = MappingType("State", str)
    cis_id = MappingType("Affiliate ID", int)
    official_name = MappingType("Affiliate's Official Name", str)
    address_street = MappingType("Address (# and Street)", str)
    address_city = MappingType("City", str)
    address_state = MappingType("State2", str)
    address_postcode = MappingType("Zip", str)
    shipping_address = MappingType("Shipping Address", str)
    phone_number = MappingType("Phone", str)
    fax_number = MappingType("Fax", str)
    website = MappingType("Website Address", str)
    affiliate_location = MappingType("Affiliate Location", str)


class AffiliateEOYFields(PandasMapper):
    districts = MappingType("Name(s) of district(s) served", str)
    executive_director_name = MappingType("Executive Director name", str)
    executive_director_email = MappingType("ED Email Address", str)
    program_lead_name = MappingType("CIS Model/Programming Name", str)
    program_lead_email = MappingType("CIS Model/Programming Email", str)

    budget_total = MappingType("TOTAL BUDGET (auto)", int)

    staff_fulltime_affiliate = MappingType("FT CIS pd affiliate staff", int)
    staff_parttime_affiliate = MappingType("PT CIS pd affiliate staff", int)
    staff_fulltime_non_affiliate = MappingType("FT Non-CIS pd affiliate staff", int)
    staff_parttime_non_affiliate = MappingType("PT Non-CIS pd affiliate staff", int)
    staff_fulltime_americorps = MappingType("FT AmeriCorps affiliate staff", int)
    staff_parttime_americorps = MappingType("PT AmeriCorps affiliate staff", int)

    funding_public_federal = MappingType("Fed - TOTAL (auto)", int)
    funding_public_state = MappingType("State - TOTAL (auto)", int)
    funding_public_city = MappingType("City - TOTAL (auto)", int)
    funding_public_school_district = MappingType("Sch Dis - TOTAL (auto)", int)
    funding_private_corporate = MappingType("Corp - TOTAL (auto)", int)
    funding_private_foundation = MappingType("Fdn - TOTAL (auto)", int)
    funding_private_board = MappingType("Board - TOTAL (auto)", int)
    funding_private_individual = MappingType("Indiv - TOTAL (auto)", int)
    funding_private_events = MappingType("Events - TOTAL (auto)", int)
    funding_private_cis_national = MappingType("CIS Natl - TOTAL (auto)", int)
    funding_private_cis_state_office = MappingType("State Office - TOTAL (auto)", int)
    funding_private_npo = MappingType("NPO - TOTAL (auto)", int)
    funding_private_other = MappingType("Other - TOTAL (auto)", int)


class SchoolStudentEOYFields(PandasMapper):
    """Maps model fields from the DataFrame to model/column names

    This maps data from two worksheets which in Pandas are merged into one dataframe

    """

    site_type = MappingType("Site Type", str)
    location = MappingType("Location (NCES)", str)
    location_model = MappingType("CIS Model or GYS?", str)
    student_enrollment = MappingType("Student Enrollment", int)

    service_academic_assistance = MappingType("Academic Assistance", str)
    service_basic_needs = MappingType("Basic Needs", str)
    service_behavior_intervention = MappingType("Behavior Intervention", str)
    service_college_career_prep = MappingType("College/ Career Prep", str)
    service_comm_service = MappingType("Comm Service/S-L", str)
    service_enrichment = MappingType("Enrichment", str)
    service_family_engagement = MappingType("Family Engagement", str)
    service_life_skills = MappingType("Life Skills", str)
    service_physical_fitness_health = MappingType("Physical Fitness/Health", str)
    service_prof_mental_health = MappingType("Prof Mental Health", str)

    students_case_managed = MappingType("# Case Managed Students", int)
    students_total = MappingType("# Students w/ whole school support", int)

    students_female_american_indian = MappingType("Students, Female - American Indian", int)
    students_female_asian = MappingType("Students, Female - Asian", int)
    students_female_black = MappingType("Students, Female - Black", int)
    students_female_hispanic = MappingType("Students, Female - Hispanic", int)
    students_female_white = MappingType("Students, Female - White", int)
    students_female_two_or_more_races = MappingType("Students, Female - Two or More Races", int)
    students_female_other = MappingType("Students, Female - Other", int)
    students_female_unknown = MappingType("Students, Female - Unknown", int)
    students_male_american_indian = MappingType("Students, Male - American Indian", int)
    students_male_asian = MappingType("Students, Male - Asian", int)
    students_male_black = MappingType("Students, Male - Black", int)
    students_male_hispanic = MappingType("Students, Male - Hispanic", int)
    students_male_white = MappingType("Students, Male - White", int)
    students_male_two_or_more_races = MappingType("Students, Male - Two or More Races", int)
    students_male_other = MappingType("Students, Male - Other", int)
    students_male_unknown = MappingType("Students, Male - Unknown", int)
    students_unknown_race_gender = MappingType("Students, Unknown Race/Gender", int)

    students_k_11_promoted = MappingType("K-11 Promoted", int)
    students_k_11_retained = MappingType("K-11 Retained", int)
    students_k_11_dropped_out = MappingType("K-11 Dropped Out", int)
    students_k_11_transferred = MappingType("K-11 Transferred", int)
    students_k_11_ged = MappingType("K-11 GED", int)
    students_k_11_expelled = MappingType("K-11 Expelled", int)
    students_k_11_incarcerated = MappingType("K-11 Incarcerated", int)
    students_k_11_deceased = MappingType("K-11 Deceased", int)
    students_k_11_other = MappingType("K-11 Other", int)
    students_k_11_unknown = MappingType("K-11 Unknown", int)
    students_grade_12_graduated = MappingType("Grade 12 Graduated", int)
    students_grade_12_retained = MappingType("Grade 12 Retained", int)
    students_grade_12_dropped_out = MappingType("Grade 12 Dropped Out", int)
    students_grade_12_transferred = MappingType("Grade 12 Transferred", int)
    students_grade_12_ged = MappingType("Grade 12 GED", int)
    students_grade_12_expelled = MappingType("Grade 12 Expelled", int)
    students_grade_12_incarcerated = MappingType("Grade 12 Incarcerated", int)
    students_grade_12_deceased = MappingType("Grade 12 Deceased", int)
    students_grade_12_other = MappingType("Grade 12 Other", int)
    students_grade_12_unknown = MappingType("Grade 12 Unknown", int)

    students_served_frpl = MappingType("eligible FRPL", int)
    students_served_ell = MappingType("ELL - Yes", int)
    students_served_foster = MappingType("Foster care/Group home - Yes", int)
    students_served_homeless = MappingType("Homeless - Yes", int)
    students_served_lgbt = MappingType("LGBT - Yes", int)
    students_served_pregnant_parenting = MappingType("Pregnant/ Parenting - Yes", int)
    students_served_special_education = MappingType("Special Education - Yes", int)
    students_served_substance_abuse = MappingType("Substance abuse - Yes", int)
    students_served_adjudicated_youth = MappingType("Adj Youth - Yes", int)
    students_served_child_of_military = MappingType("Child of military - Yes", int)
    students_served_gang = MappingType("Gang Involvement - Yes", int)
    students_served_incarcerated_parent = MappingType("Incarcerated parent - Yes", int)

    students_grade_prek = MappingType("Pre-K", int)
    students_grade_k = MappingType("Kindergarten", int)
    students_grade_1 = MappingType("1st Grade", int)
    students_grade_2 = MappingType("2nd Grade", int)
    students_grade_3 = MappingType("3rd Grade", int)
    students_grade_4 = MappingType("4th Grade", int)
    students_grade_5 = MappingType("5th Grade", int)
    students_grade_6 = MappingType("6th Grade", int)
    students_grade_7 = MappingType("7th Grade", int)
    students_grade_8 = MappingType("8th Grade", int)
    students_grade_9 = MappingType("9th Grade", int)
    students_grade_10 = MappingType("10th Grade", int)
    students_grade_11 = MappingType("11th Grade", int)
    students_grade_12 = MappingType("12th Grade", int)
