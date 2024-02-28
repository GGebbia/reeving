from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import process_invoices

from .models import Invoice
from .serializer import InvoiceSerializer, UploadedFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        queryset = Invoice.objects.all()
        customer_name = self.request.query_params.get('customer', None)
        if customer_name:            
            queryset = queryset.filter(customer=customer_name)
        
        return queryset


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()

            # Start celery process
            process_invoices.delay(filepath=str(settings.BASE_DIR) + file_serializer.data['file'])
            return Response({"message": "Data is being processed"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
