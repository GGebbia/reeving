from django.test import TestCase
from invoice_processor.tasks import process_invoices
from django.conf import settings

class ProcessInvoicesTaskTest(TestCase):
    
    def test_filepath_not_exists(self):
        """Test process_invoices raises FileNotFoundError when file does not exists."""
        invalid_filepath = "./test.xlsx"
        with self.assertRaises(FileNotFoundError):
            process_invoices(invalid_filepath)

    def test_xlsx_extension_e2e(self):
        """Test process_invoices end to end with XLSX extension file"""
        xlsx_filepath = "./media/test/test_invoices.xlsx"
        result = process_invoices(xlsx_filepath)

        self.assertEqual(result, True)
        self

    def test_csv_extension_e2e(self):
        """Test process_invoices end to end with CSV extension file"""
        csv_filepath = "./media/test/test_invoices.csv"
        result = process_invoices(csv_filepath)
        self.assertEqual(result, True)

    # def test_invalid_extension(self):
    #     pass