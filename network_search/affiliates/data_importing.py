"""
Functionality specific to importing affiliate data

These enumerated types map a model field name (the enum name) to
the column name (the enum value) in the spreadsheet data source.
"""

from network_search.core import choices


class ImportingChoice(choices.Choice):

    @classmethod
    def defaults(cls, data_row):
        return {
            i.name: data_row[i.value]
            for i in cls
        }


class AffiliateFields(ImportingChoice):
    """Maps model fields to spreadsheet (and DataFrame) column names

    Does NOT include "name" as this is used for a primary lookup
    """
    state = "State"
    cis_id = "Affiliate ID"
    official_name = "Affiliate's Official Name"
    address_street = "Address (# and Street)"
    address_city = "City"
    address_state = "State2"
    address_postcode = "Zip"
    shipping_address = "Shipping Address"
    phone_number = "Phone"
    fax_number = "Fax"
    website = "Website Address"
    affiliate_location = "Affiliate Location"


class AffiliateEOYFields(ImportingChoice):

    districts = "Name(s) of district(s) served"
    executive_director_name = "Executive Director name"
    executive_director_email = "ED Email Address"
    program_lead_name = "CIS Model/Programming Name"
    program_lead_email = "CIS Model/Programming Email"

    budget_total = "TOTAL BUDGET (auto)"

    staff_fulltime_affiliate = "FT CIS pd affiliate staff"
    staff_parttime_affiliate = "PT CIS pd affiliate staff"
    staff_fulltime_non_affiliate = "FT Non-CIS pd affiliate staff"
    staff_parttime_non_affiliate = "PT Non-CIS pd affiliate staff"
    staff_fulltime_americorps = "FT AmeriCorps affiliate staff"
    staff_parttime_americorps = "PT AmeriCorps affiliate staff"

    funding_public_federal = "Fed - TOTAL (auto)"
    funding_public_state = "State - TOTAL (auto)"
    funding_public_city = "City - TOTAL (auto)"
    funding_public_school_district = "Sch Dis - TOTAL (auto)"
    funding_private_corporate = "Corp - TOTAL (auto)"
    funding_private_foundation = "Fdn - TOTAL (auto)"
    funding_private_board = "Board - TOTAL (auto)"
    funding_private_individual = "Indiv - TOTAL (auto)"
    funding_private_events = "Events - TOTAL (auto)"
    funding_private_cis_national = "CIS Natl - TOTAL (auto)"
    funding_private_cis_state_office = "State Office - TOTAL (auto)"
    funding_private_npo = "NPO - TOTAL (auto)"
    funding_private_other = "Other - TOTAL (auto)"


class SchoolStudentEOYFields(ImportingChoice):
    """Maps model fields from the DataFrame to model/column names

    This maps data from two worksheets which in Pandas are merged into one dataframe

    """

    site_type = "Site Type"
    location = "Location (NCES)"
    location_model = "CIS Model or GYS?"
    student_enrollment = "Student Enrollment"

    service_academic_assistance = "Academic Assistance"
    service_basic_needs = "Basic Needs"
    service_behavior_intervention = "Behavior Intervention"
    service_college_career_prep = "College/ Career Prep"
    service_comm_service = "Comm Service/S-L"
    service_enrichment = "Enrichment"
    service_family_engagement = "Family Engagement"
    service_life_skills = "Life Skills"
    service_physical_fitness_health = "Physical Fitness/Health"
    service_prof_mental_health = "Prof Mental Health"

    students_case_managed = "# Case Managed Students"
    students_total = "# Students w/ whole school support"

    students_female_american_indian = "Students, Female - American Indian"
    students_female_asian = "Students, Female - Asian"
    students_female_black = "Students, Female - Black"
    students_female_hispanic = "Students, Female - Hispanic"
    students_female_white = "Students, Female - White"
    students_female_two_or_more_races = "Students, Female - Two or More Races"
    students_female_other = "Students, Female - Other"
    students_female_unknown = "Students, Female - Unknown"
    students_male_american_indian = "Students, Male - American Indian"
    students_male_asian = "Students, Male - Asian"
    students_male_black = "Students, Male - Black"
    students_male_hispanic = "Students, Male - Hispanic"
    students_male_white = "Students, Male - White"
    students_male_two_or_more_races = "Students, Male - Two or More Races"
    students_male_other = "Students, Male - Other"
    students_male_unknown = "Students, Male - Unknown"
    students_unknown_race_gender = "Students, Unknown Race/Gender"

    students_k_11_promoted = "K-11 Promoted"
    students_k_11_retained = "K-11 Retained"
    students_k_11_dropped_out = "K-11 Dropped Out"
    students_k_11_transferred = "K-11 Transferred"
    students_k_11_ged = "K-11 GED"
    students_k_11_expelled = "K-11 Expelled"
    students_k_11_incarcerated = "K-11 Incarcerated"
    students_k_11_deceased = "K-11 Deceased"
    students_k_11_other = "K-11 Other"
    students_k_11_unknown = "K-11 Unknown"
    students_grade_12_graduated = "Grade 12 Graduated"
    students_grade_12_retained = "Grade 12 Retained"
    students_grade_12_dropped_out = "Grade 12 Dropped Out"
    students_grade_12_transferred = "Grade 12 Transferred"
    students_grade_12_ged = "Grade 12 GED"
    students_grade_12_expelled = "Grade 12 Expelled"
    students_grade_12_incarcerated = "Grade 12 Incarcerated"
    students_grade_12_deceased = "Grade 12 Deceased"
    students_grade_12_other = "Grade 12 Other"
    students_grade_12_unknown = "Grade 12 Unknown"

    students_served_frpl = "eligible FRPL"
    students_served_ell = "ELL - Yes"
    students_served_foster = "Foster care/Group home - Yes"
    students_served_homeless = "Homeless - Yes"
    students_served_lgbt = "LGBT - Yes"
    students_served_pregnant_parenting = "Pregnant/ Parenting - Yes"
    students_served_special_education = "Special Education - Yes"
    students_served_substance_abuse = "Substance abuse - Yes"
    students_served_adjudicated_youth = "Adj Youth - Yes"
    students_served_child_of_military = "Child of military - Yes"
    students_served_gang = "Gang Involvement - Yes"
    students_served_incarcerated_parent = "Incarcerated parent - Yes"
