============
Data choices
============

The `network_search.core.choices` module uses Python's Enum class to provide sensible *coded* blocks,
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

Displaying in templates
=======================

Displaying the approriate label for a given stored value, e.g. showing "female" for "f"
is simple when working with traditional `model.CharField` fields using choices. However
the `get_<field_name>_display` method will not work on an `ArrayField`.

For this this reason the `choice_display` in the `choice_tags` library exists.::

    {% load choice_tags %}

    {% for race in object.race %}
        {{ race|choice_display:"Race" }}
    {% endfor %}

The `choice_display` filter takes two arguments, the implicit value before the pipe and then second
which is the **case sensitive** name of the choice enum class from which to extract the label.

If this class name is wrong, you will see an AttributeError. This is intentional as noted in the
class documentation.

Incorrect name values, on the other hand, will only result in a logged error and on the front-end
the user will simply see the raw value provided.
