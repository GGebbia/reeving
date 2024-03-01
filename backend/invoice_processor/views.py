from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import process_invoices
from .pagination import StandardResultsSetPagination

from .models import Invoice
from .serializer import InvoiceSerializer, UploadedFileSerializer, RevenueSourceTotalsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db.models import Sum, F, ExpressionWrapper, DecimalField

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):
        """
        Override of get_queryset function. Doing so, the GET /api/invoices/ endpoint accepts querying
        over customer.
        If customer_name is not set in the query params it will return all elements.
        """
        queryset = Invoice.objects.all()
        customer_name = self.request.query_params.get('customer', None)
        if customer_name:            
            queryset = queryset.filter(customer=customer_name)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override of retrieve function. This hack ensures that a making requests to /api/invoices/<pk>/ will
        return a list object (of a single element).
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response([serializer.data])


class FileUploadView(APIView):

    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        """
        Override of post function.
        Check that a file upload is valid using UploadedFileSerializer.
        Stores the file under MEDIA_ROOT directory and start the Celery process by calling process_invoices() method.
        """
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file = file_serializer.validated_data['file']
            filepath = f"{str(settings.BASE_DIR)}/media/data/{file.name}"
            default_storage.save(filepath, ContentFile(file.read()))

            # Start celery process
            process_invoices.delay(filepath=filepath)
            return Response({"message": "Data is being processed"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RevenueSourceTotalsView(APIView):

    def get(self, request):
        """
        Override of get function.
        It aggregates over the set of Invoices grouped by revenue_source the following fields:
            - total_value: Sum of each invoice value
            - total_advance: Sum of [value - (value * haircut_percent) / 100]. Ask Ana if this is correct?
            - total_expected_fee: Given the Advance formulae above, multiply it by daily_fee_percent and the expected payment duration. Is this correct?
        """
        revenue_source_qs = Invoice.objects.values('revenue_source').annotate(
            total_value=Sum('value'),
            total_advance=Sum(ExpressionWrapper(
                F('value') - (F('value') * F('haircut_percent') / 100),
                output_field=DecimalField(max_digits=10, decimal_places=3))),
            total_expected_fee=Sum(ExpressionWrapper(
                (F('value') - (F('value') *F('haircut_percent') / 100)) * F('daily_fee_percent')/ 100 * F('expected_payment_duration'),
                output_field=DecimalField(max_digits=10, decimal_places=3)))
        ).order_by('total_value')

        # Serialize the data
        serializer = RevenueSourceTotalsSerializer(revenue_source_qs, many=True)
        return Response(serializer.data)