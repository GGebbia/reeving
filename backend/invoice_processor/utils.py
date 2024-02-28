import os
import pandas as pd
from .models import Invoice

from celery import shared_task

@shared_task
def process_invoices(filepath: str) -> None:
    """
    Reads an excel file and stores in DB the invoice
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file at {filepath} does not exist")

    invoices_dataframe: pd.DataFrame = pd.read_excel(filepath)
    invoices_dataframe = invoices_dataframe.rename(columns=lambda x: x.lower().replace(' ', '_'))
    for idx, row in invoices_dataframe.iterrows():
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

        # https://docs.djangoproject.com/en/5.0/ref/models/instances/#how-django-knows-to-update-vs-insert
        invoice.save()
