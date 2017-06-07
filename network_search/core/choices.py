"""
Common choices

"""
from typing import Any, Dict, List, Tuple


def sorted_choices(choice_tuple: List[Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
    """Return a choice list sorted by name"""
    return sorted(choice_tuple, key=lambda x: x[1])


def inverted_choices(choice_tuple: List[Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
    """Returns a list of the reversed tuples

    This is expected to be useful where matching data for imports
    """
    return [
        (i[1], i[0]) for i in choice_tuple
    ]


def populator(choice_tuple: List[Tuple[Any, Any]]) -> Dict[Any, Any]:
    """Returns a dictionary of the tuples by inversion

    This is expected to be useful where matching data for imports
    """
    return {
        i[1]: i[0] for i in choice_tuple
    }


GRADES = [
    ('ec', 'Early Childhood Education'),
    ('el', 'Elementary'),
    ('ms', 'Middle School'),
    ('hs', 'High School'),
    ('ps', 'Post-Secondary'),
]

GENDER = [
    ('f', 'female'),
    ('m', 'male'),
]

RACE = [
    ('am', 'American Indian'),
    ('as', 'Asian'),
    ('bl', 'Black'),
    ('hi', 'Hispanic'),
    ('wh', 'White'),
    ('2', 'Two or more races'),
]

REGIONS = [
    ('n', 'Nationwide'),
    ('i', 'International'),
]

STUDENT_NEEDS = [
    ('bi', 'Behavioral Issues'),
    ('att', 'Attendance Issues/Chronically Absent'),
    ('do', 'At risk of dropping out'),
    ('phn', 'Physical Health Needs'),
    ('sel', 'SEL Needs'),
    ('mh', 'Mental Health Needs'),
    ('ac', 'Academic Needs'),
    ('hr', 'High Risk Behavior'),
    ('pr', 'Pregnant/Parenting'),
    ('ccr', 'College/Career Readiness'),
    ('pfe', 'Parent/Family Engagement'),
    ('ell', 'English Language Learners'),
    ('hfy', 'Homesless/Foster Youth'),
    ('juv', 'At risk of entering juvenile justice system'),
]


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
