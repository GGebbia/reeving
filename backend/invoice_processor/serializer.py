from rest_framework import serializers
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model.
    """
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

# Alternatively we could have a model serializer and have trace of uploaded files.
class UploadedFileSerializer(serializers.Serializer):
    """
    Serializer for file upload.

    It uses FileField representation to process files. 
    https://www.django-rest-framework.org/api-guide/fields/#filefield
    """
    file = serializers.FileField()


class RevenueSourceTotalsSerializer(serializers.Serializer):
    """
    Serializer to represent per-revenue source Totals, Advance and Excepted Fee.

    It aggregates totals, advance and expected_fee of a set of Invoice instances based on the revenue source.
    """
    revenue_source = serializers.CharField(max_length=100)
    total_value = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_advance = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_expected_fee = serializers.DecimalField(max_digits=10, decimal_places=3)