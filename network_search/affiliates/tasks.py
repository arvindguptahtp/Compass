"""

"""

import logging
import time

import pandas as pd
from celery import shared_task

from network_search.affiliates import models

logger = logging.getLogger(__name__)


@shared_task
def process_data_upload(excel_upload_pk):

    # Sleeping here b/c of issues in dev - it's as if the primary key was returned
    # before the data was committed to the database... which may be the case! If this
    # is eagerly evaluated and the transaction is only fully committed after the response
    # is rendered (?) then the database could be queried for the data before it's even
    # committed into the table. A better strategy would be to rely on Django's own
    # `transaction.on_commit`.
    time.sleep(1)

    try:
        data_upload = models.ExcelUpload.objects.get(pk=excel_upload_pk)
    except models.ExcelUpload.DoesNotExist:
        logger.error("No upload found for affiliate excel: {}".format(excel_upload_pk))
        logger.error("Total: {}".format(models.ExcelUpload.objects.all().count()))
        return

    try:
        affiliates_list = pd.read_excel(data_upload.data_file, sheetname=0, header=0, skiprows=[0])
    except Exception as e:
        data_upload.status = 'f'
        data_upload.save()
        logger.exception("Error reading Affiliates file/worksheet")
        raise
        # return

    print("DONE")


