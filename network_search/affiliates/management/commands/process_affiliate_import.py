from django.core.management.base import BaseCommand

from network_search.affiliates.models import ExcelUpload
from network_search.affiliates.tasks import process_data_upload


class Command(BaseCommand):
    help = 'Process a saved import'

    def handle(self, *args, **options):

        process_data_upload(ExcelUpload.objects.latest('pk').pk)
