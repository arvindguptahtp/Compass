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

"""
from enum import Enum
from typing import Any
from typing import List
from typing import Dict
from typing import Tuple


class Choice(Enum):

    @classmethod
    def as_choices(cls):
        return [
            (child.name, child.value)
            for child in cls
        ]


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


STUDENT_CHARACTERISTICS = [
    ('frpl', 'Eligible for FRPL'),
    ('ay', 'Adjudicated Youth'),
    ('mil', 'Child of Active Duty Military'),
    ('ell', 'English Language Learners'),
    ('fos', 'Foster Care/Group Home'),
    ('gang', 'Gang Involvement'),
    ('hl', 'Homeless'),
    ('ip', 'Incarcerated Parent'),
    ('lgbt', 'LGBT'),
    ('pp', 'Pregnant/Parenting'),
    ('se', 'Special Education'),
    ('sa', 'Substance Abuse'),
    ('na', 'Not Applicable'),
]


TIERS_OF_SERVICE = [
    ('1', 'Tier I'),
    ('2', 'Tier II'),
    ('3', 'Tier III'),
]


SETTING = [
    ('sch', 'School'),
    ('hf', 'Home/Family'),
    ('co', 'Community'),
    ('as', 'Afterschool'),
    ('sp', 'Summer Program'),
]


CORE_SERVICES = [
    ('aa', 'Academic Assistance'),
    ('bn', 'Basic Needs'),
    ('bi', 'Behavioral Interventions'),
    ('ccp', 'College and Career Preparation'),
    ('csl', 'Community and Service Learning'),
    ('en', 'Enrichment'),
    ('fe', 'Family Engagement'),
    ('ls', 'Life Skills/Social Development'),
    ('pmh', 'Professional Mental Health'),
    ('pph', 'Professional Physical Health'),
]


TIERS_OF_EVIDENCE = [
    ('1', 'Strong evidence'),
    ('2', 'Moderate evidence'),
    ('3', 'Promising evidence (High)'),
    ('4', 'Promising evidence (low)'),
    ('5', 'Demonstrates a rationale/Research-building'),
]
