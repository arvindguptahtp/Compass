"""Simple tests for URL configuration"""

from django.core.urlresolvers import reverse


def test_partner_list():
    assert reverse("partner_list")


def test_partner_detail():
    assert reverse("partner_detail", kwargs={"pk": 487})


def test_partner_pdf():
    assert reverse("partner_pdf", kwargs={"pk": 487})


def test_program_list():
    assert reverse("program_list")


def test_program_detail():
    assert reverse("program_detail", kwargs={"pk": 487})


def test_program_pdf():
    assert reverse("program_pdf", kwargs={"pk": 487})


def test_affiliate_list():
    assert reverse("affiliate_list")


def test_affiliate_detail():
    assert reverse("affiliate_detail", kwargs={"pk": 487})


def test_affiliate_pdf():
    assert reverse("affiliate_pdf", kwargs={"pk": 487})
