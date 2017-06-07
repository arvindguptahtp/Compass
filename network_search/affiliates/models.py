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
    url_name = "affiliate_detail"
    search_content_fields = ["name"]

    affiliates = AffiliateQueryset.as_manager()
    objects = affiliates
