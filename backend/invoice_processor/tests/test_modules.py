import datetime
from django.db import IntegrityError
from django.test import TestCase
from invoice_processor.models import Invoice
from decimal import Decimal


class InvoiceModelTest(TestCase):

    def test_model_creation(self):
        """Test invoice model can be created successfully with valid fields."""

        invoice = Invoice.objects.create(
            invoice_number=7107,
            date="2023-10-23",
            customer="Playcrows",
            revenue_source="SuperAmazing",
            value=Decimal('7277.746'),
            haircut_percent=10,
            daily_fee_percent=Decimal('0.125'),
            currency='USD',
            expected_payment_duration=60
        )

        invoices = Invoice.objects.all()
        self.assertEqual(invoices.count(), 1)

        invoice = invoices[0]
        self.assertEqual(invoice.invoice_number, 7107)
        self.assertIsInstance(invoice.date, datetime.date)
        self.assertEqual(str(invoice.date), "2023-10-23")
        self.assertEqual(invoice.customer, "Playcrows")
        self.assertEqual(invoice.revenue_source, "SuperAmazing")
        self.assertEqual(invoice.value, Decimal("7277.746"))
        self.assertEqual(invoice.haircut_percent, 10)
        self.assertEqual(invoice.daily_fee_percent, Decimal("0.125"))
        self.assertEqual(invoice.currency, 'USD')
        self.assertEqual(invoice.expected_payment_duration, 60)

    def test_str_representation(self):
        "Test invoice model __str__ representation"
        invoice = Invoice.objects.create(
            invoice_number=7107,
            date="2023-10-23",
            customer="Playcrows",
            revenue_source="SuperAmazing",
            value=Decimal('7277.746'),
            haircut_percent=10,
            daily_fee_percent=Decimal('0.125'),
            currency='USD',
            expected_payment_duration=60
        )

        self.assertEqual(str(invoice), "Invoice 7107 - Playcrows - 2023-10-23")

    def test_unique_constraint(self):
        """Test the unicity constraint on invoice_mumber and customer fields"""

        Invoice.objects.create(
            invoice_number=7107,
            date="2023-10-23",
            customer="Playcrows",
            revenue_source="SuperAmazing",
            value=Decimal('7277.746'),
            haircut_percent=10,
            daily_fee_percent=Decimal('0.125'),
            currency='USD',
            expected_payment_duration=60
        )

        with self.assertRaises(IntegrityError):
            Invoice.objects.create(
                invoice_number=7107,
                date="2023-10-23",
                customer="Playcrows",
                revenue_source="SuperAmazing",
                value=Decimal('7277.746'),
                haircut_percent=10,
                daily_fee_percent=Decimal('0.125'),
                currency='USD',
                expected_payment_duration=60
            )

        