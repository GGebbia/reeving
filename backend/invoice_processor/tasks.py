import os
import pandas as pd
from .models import Invoice
import time
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

XLSX_EXTENSION = ".xlsx"
CSV_EXTENSION = ".csv"

@shared_task
def process_invoices(filepath: str) -> bool:
    """
    Reads an excel/csv file and stores in DB the invoice
    """
    
    start_time = time.time()
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file at {filepath} does not exist")
    
    try:
        extension = os.path.splitext(filepath)[1]
        if extension == XLSX_EXTENSION:
            invoices_dataframe: pd.DataFrame = pd.read_excel(filepath)
        elif extension == CSV_EXTENSION:
            invoices_dataframe: pd.DataFrame = pd.read_csv(filepath, )
        else:
            # This should never happen since it is already controlled in frontend.
            logger.error(f"Unsupported file type: {extension}.")
            return False
        
        logger.info(f"File reading time = {time.time() - start_time}")
        invoices_dataframe = invoices_dataframe.rename(columns=lambda x: x.lower().replace(' ', '_'))

        # Avoid duplicates
        # invoices_dataframe = invoices_dataframe.drop_duplicates()

        invoices = []
        for _, row in invoices_dataframe.iterrows():

            invoice: Invoice = Invoice(
                invoice_number=row['invoice_number'],
                date=row['date'],
                customer=row['customer'],
                revenue_source=row['revenue_source'],
                value=row['value'],
                haircut_percent=row['haircut_percent'],
                daily_fee_percent=row['daily_fee_percent'],
                currency=row['currency'],
                expected_payment_duration=row['expected_payment_duration']
            )
            invoices.append(invoice)

        Invoice.objects.bulk_create(invoices, ignore_conflicts=True)
        logger.info(f"Finished inserting in database = {time.time() - start_time}")

        return True
    except Exception as e:
        logger.error(e)
        return False