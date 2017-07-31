

import logging

from django import template
from django.template.defaultfilters import stringfilter
from localflavor.us.us_states import USPS_CHOICES

register = template.Library()

logger = logging.getLogger(__name__)


@register.filter
@stringfilter
def us_state(abbrev: str) -> str:
    states = dict(USPS_CHOICES)
    try:
        return states[abbrev.upper()]
    except KeyError:
        logger.error("No state matches the abbreviation '{}'".format(abbrev))
        return abbrev


@register.filter
@stringfilter
def linkable(link: str) -> str:
    """Prepends http:// to links"""
    if not link or link.startswith("http"):
        return link
    return "http://" + link
