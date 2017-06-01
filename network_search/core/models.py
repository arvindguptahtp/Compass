from model_utils.models import TimeStampedModel
from django.db import models


class Link(TimeStampedModel):
    title = models.CharField(max_length=100, blank=True, null=True, help_text="Optional visible for link")
    url = models.URLField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

    @property
    def label(self):
        """Returns a label appropriate for displaying on the front end"""
        return self.title if self.title else self.url
