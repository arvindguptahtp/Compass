from model_utils.models import TimeStampedModel
from model_utils.models import TimeStampedModel

from network_search.core.models import Link, BaseResource, ResourceQueryset


class AffiliateQueryset(ResourceQueryset):
    def search(self, **kwargs):
        qs = super().search(**kwargs)
        return qs


class Affiliate(BaseResource):
    """
    Represents the steady data for an affiliates directory
    
    All EOY data is related to this model
    """
    affiliates = AffiliateQueryset.as_manager()
    objects = affiliates
