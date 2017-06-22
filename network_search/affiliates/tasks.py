"""
Task processing for upload processing
"""

import logging
import time

import pandas as pd
from celery import shared_task

from network_search.affiliates import models

logger = logging.getLogger(__name__)


AFFILIATE_SHEET_NAME = 'Affiliate_Data'
SCHOOL_SHEET_NAME = 'School_Data'
STUDENT_SHEET_NAME = 'Student_Data'


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
        affiliates_workbook = pd.read_excel(
            data_upload.data_file,
            sheetname=None,
            header=0,
        )
    except Exception as e:
        data_upload.status = data_upload.FAILED
        data_upload.message = "{}".format(e)
        data_upload.save()
        logger.exception("Error reading Affiliates file/worksheet")
        return

    affiliate_messages = []

    affiliate_data = affiliates_workbook[AFFILIATE_SHEET_NAME]
    school_data = affiliates_workbook[SCHOOL_SHEET_NAME]
    student_data = affiliates_workbook[STUDENT_SHEET_NAME]
    school_student_data = school_data.merge(student_data, on=["Affiliate Name", "School Name"])

    logger.debug("Iterating over dataframe...")

    for index, row in affiliate_data.iterrows():
        logger.debug("...over row {} now...".format(index))
        try:
            affiliate, created = models.Affiliate.affiliates.get_or_create(
                name=row['Affiliate Name'],
                defaults={
                    'state': row['State'],
                    'cis_id': row['Affiliate ID'],
                    'official_name': row["Affiliate's Official Name"],
                    'address_street': row['Address (# and Street)'],
                    'address_city': row['City'],
                    'address_state': row['State2'],
                    'address_postcode': row['Zip'],
                    'shipping_address': row['Shipping Address'],
                    'phone_number': row['Phone'],
                    'fax_number': row['Fax'],
                    'website': row['Website Address'],
                    'affiliate_location': row['Affiliate Location'],
                },
            )
            logger.info("{} affiliate '{}'".format("Created" if created else "Found", affiliate))
        except Exception as e:
            logger.exception("Error processing data row in affiliate Excel upload")
            affiliate_messages.append('Error processing row: {}'.format(e))
        else:

            affiliate_eoy_data, created = models.AffiliateEOYData.objects.get_or_create(
                affiliate=affiliate,
                year=data_upload.year,
                defaults={
                    'districts': row['Name(s) of district(s) served'],
                },
            )
            logger.info("{} affiliate EOY data '{}'".format("Created" if created else "Found", affiliate_eoy_data))

            affiliate_schools = school_student_data.loc[school_student_data["Affiliate Name"] == affiliate.name]

            logger.info("Found {} schools for affiliate {}".format(len(affiliate_schools), affiliate))

            for index, school_row in affiliate_schools.iterrows():
                logger.debug("Iterating through school data subsection now")
                try:
                    school, created = models.SchoolEOYData.objects.get_or_create(
                        affiliate_data=affiliate_eoy_data,
                        name=school_row["School Name"],
                    )
                except:
                    logger.exception("COULD NOT READ OR CREATE SCHOOL")
                else:
                    logger.info("{} {} school EOY data '{}'".format(
                        "Created" if created else "Found", data_upload.year, school))


    data_upload.status = data_upload.COMPLETED
    data_upload.message = '\n'.join(affiliate_messages)
    data_upload.save()


