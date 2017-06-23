"""
Common choices

This module uses Python's Enum class to provide sensible *coded* blocks,
obviating the need to work with error prone string literals, and to do
so in a way compatible with Django's expected `choices` value.

The `Choice` class is used here to ensure that any enumerated type can
be packaged as a list of tuples with strings.

In order to make this work and reduce verbosity, the attribute names are
shortened to what should be used in the database. It would be nicer to
use something like::

    class Gender(Enum):
        male = SomeNamedTuple('m', 'Male')
        female = SomeNamedTuple('f', 'Female')

But this leads to more difficult to read code.

Note that a "member" of an enum has two attributes:

    - name
    - value

The `name` attribute refers to the accessible name of the attribute, and
`value` refers to the string literal that is associated with it.

"""
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple


class Choice(Enum):

    @classmethod
    def as_choices(cls):
        return [
            (child.name, child.value)
            for child in cls
        ]

    @classmethod
    def all_names(cls):
        return [child.name for child in cls]

    @classmethod
    def all_values(cls):
        return [child.value for child in cls]

    def lower(self):
        return self.value.replace(" ", "_").lower()


def sorted_choices(choice_tuple: List[Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
    """Return a choice list sorted by name"""
    return sorted(choice_tuple, key=lambda x: x[1])


def populator(choice_selections: Choice) -> Dict[str, str]:
    """Returns a dictionary of the tuples by inversion

    This is expected to be useful where matching data for imports
    """
    return {
        i.value: i.name for i in choice_selections
    }


class Grades(Choice):
    ec = 'Early Childhood Education'
    el = 'Elementary'
    ms = 'Middle School'
    hs = 'High School'
    ps = 'Post-Secondary'
    cm = 'Combined (any other K-12 combination)'


class Gender(Choice):
    f = 'female'
    m = 'male'


class Race(Choice):
    am = 'American Indian'
    asn = 'Asian'
    bl = 'Black'
    his = 'Hispanic'
    wh = 'White'
    two = 'Two or more races'


class Regions(Choice):
    n = 'Nationwide'
    i = 'International'


class StudentNeeds(Choice):
    bi = 'Behavioral Issues'
    att = 'Attendance Issues/Chronically Absent'
    do = 'At risk of dropping out'
    phn = 'Physical Health Needs'
    sel = 'SEL Needs'
    mh = 'Mental Health Needs'
    ac = 'Academic Needs'
    hr = 'High Risk Behavior'
    pr = 'Pregnant/Parenting'
    ccr = 'College/Career Readiness'
    pfe = 'Parent/Family Engagement'
    ell = 'English Language Learners'
    hfy = 'Homeless/Foster Youth'
    juv = 'At risk of entering juvenile justice system'


class StudentCharacteristics(Choice):
    frpl = 'Eligible for FRPL'
    ay = 'Adjudicated Youth'
    mil = 'Child of Active Duty Military'
    ell = 'English Language Learners'
    fos = 'Foster Care/Group Home'
    gang = 'Gang Involvement'
    hl = 'Homeless'
    ip = 'Incarcerated Parent'
    lgbt = 'LGBT'
    pp = 'Pregnant/Parenting'
    se = 'Special Education'
    sa = 'Substance Abuse'
    na = 'Not Applicable'


class TiersOfService(Choice):
    i = 'Tier I'
    ii = 'Tier II'
    iii = 'Tier III'


class Setting(Choice):
    sch = 'School'
    hf = 'Home/Family'
    co = 'Community'
    aft = 'Afterschool'
    sp = 'Summer Program'


class CoreServices(Choice):
    aa = 'Academic Assistance'
    bn = 'Basic Needs'
    bi = 'Behavioral Interventions'
    ccp = 'College and Career Preparation'
    csl = 'Community and Service Learning'
    en = 'Enrichment'
    fe = 'Family Engagement'
    ls = 'Life Skills/Social Development'
    pmh = 'Professional Mental Health'
    pph = 'Professional Physical Health'


class TiersOfEvidence(Choice):
    t1 = 'Strong evidence'
    t2 = 'Moderate evidence'
    t3 = 'Promising evidence (High)'
    t4 = 'Promising evidence (low)'
    t5 = 'Demonstrates a rationale/Research-building'


class ServiceProvision(Choice):
    """Used for affiliate EOY data"""
    s1 = 'Services Provided by both CIS and Another Organization'
    s2 = 'No Services Delivered'
    s3 = 'Provided by CIS Staff'
    s4 = 'Brokered Services Delivered by Another Organization'
