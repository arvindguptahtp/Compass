import logging

from django import template
from django.template.defaultfilters import stringfilter

from network_search.core import choices

register = template.Library()

logger = logging.getLogger(__name__)


@register.filter
@stringfilter
def choice_display(name: str, choice_name: str) -> str:
    """
    Converts a string into the display value for the given choice enum

    If the 'name' doesn't exist an error is logged and then original
    value is returned. This is considered more likely to happen with
    data only to be discovered in deployed runtime. A bad choice_name
    value will however result in an AttributeError being raised as this
    is expected to be discovered in testing and/or development.

    Args:
        name: the stored value, e.g. 'm'
        choice_name: the enum class name, exactly as is, e.g. 'Gender'

    Returns:
        the display value, e.g. 'male'

    Raises:
        AttributeError if no matching choice enum class is found

    """
    choice = getattr(choices, choice_name, None)
    if choice is None:
        raise AttributeError("No choice named '{}' found.".format(choice_name))

    choice_value = getattr(choice, name, None)
    if choice_value is None:
        logger.warning("No name '{}' in '{}'.".format(name, choice_name))
        return name

    return choice_value.value


@register.inclusion_tag('core/pdf_choices.html')
def pdf_choices(options, choice):
    return {
        'options': options,
        'choice': choice,
    }
