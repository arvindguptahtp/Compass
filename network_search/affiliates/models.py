from django.db import models

from model_utils.models import TimeStampedModel


class Affiliate(TimeStampedModel):
    """
    Represents the steady data for an affiliates directory
    
    All EOY data is related to this model
    """
    name = models.CharField(max_length=400)

    def __str__(self):
        return "{}".format(self.name)
