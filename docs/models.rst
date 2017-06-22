==========================
Network Search Data Models
==========================

The network search data models can be grouped into (1) partners, (2) programs, and (3) affiilates.
Affiliate data is by far the most comprehensive and is more complicated than the former two groups.

Partners
========

There is one core partner model, `partners.Partner` which has mostly text fields and array (character) fields.

URL Links
---------

A partner has a general URL (website) but may also have other links associated with it. These are added
via a separate model, either `partners.WebinarLink` or `partners.PresentationsLink`.

Both of these are based on the abstract base model, `core.Link` which has two fields:

    1. title (optional)
    2. url (optional)

At least at the base level both fields are optional! This is because links may be used in a way that incldues
named resources that have no URL and URLs without a given name.

In both cases of the webinar and presentation, they can be accessed via appropriately named reverse names::

    some_partner.webinars.all()
    some_partner.presentations.all()

Programs
========

Programs work conceptually almost identically to partners albeit with more links.

More documentation to follow...

Affiliates
==========

`affiliates.Affiliate`
----------------------

The affiliates app includes a base `affiliates.Affiliate` model which stores "evergreen" data about an affiliate.
This does not include most end of year (EOY) reporting data.

This model stores little to no reporting data. To access that data (from the `affiliate.AffiliateEOYData` below),
use the `current_data` method on the `affiliates.Affiliate` model.::

    affiliate = Affiliate.affiliates.get(pk=page_id)
    affiliate_data = affiliate.current_data()

This will return a single `affiliates.AffiliateEOYData` instance from which other fields and methods can be
subsequently accessed or it will return `None`.

`affiliates.EndOfYear`
----------------------

Reporting data is tied to an affiliate and an `affiliates.EndOfYear` instance.

The `EndOfYear` model is used to decide *which* set of data below is included for search and for display.
In both instances only data related to the *most recent, active* `EndOfYear` will be displayed.

`affiliates.AffiliateEOYData`
-----------------------------

The reportin data is focused on the `affiliates.AffiliateEOYData` model, which has a unique relationship between
an affiliate and a reporting (EOY)
year.

To access school district info use the property methods defined on the class, `school_districts_count` and
`school_districts` as the base data is simply text.


`affiliates.SchoolEOYData`
--------------------------

School and student data is stored in `affiliates.SchoolEOYData` which relates the data for a single school
to an `affiliates.AffiliateEOYData` instance.

The `affiliates.SchoolEOYData` is where most of the 'raw' numerical data is stored, and for the most part this
should be accessed via aggregation fields on the `affiliates.AffiliateEOYData` model or via methods on the same.

`affiliates.ExcelUpload`
------------------------

This is a backend only model used to simplify the interface for processing uploaded data.
