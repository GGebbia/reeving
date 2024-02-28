from rest_framework import serializers
from .models import Invoice, UploadedFile

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'invoice_number',
            'date',
            'customer',
            'revenue_source',
            'value',
            'haircut_percent',
            'daily_fee_percent',
            'currency',
            'expected_payment_duration'
            ]

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file']