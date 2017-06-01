from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from model_utils.models import TimeStampedModel


class Program(TimeStampedModel):
    name = models.CharField(max_length=400)
    grade = ArrayField(
        models.CharField(max_length=100, blank=True),
    )

    network_use = models.ManyToManyField('affiliates.Affiliate', related_name='programs', blank=True)

    search_content = SearchVectorField()

    def __str__(self):
        return "{}".format(self.name)
