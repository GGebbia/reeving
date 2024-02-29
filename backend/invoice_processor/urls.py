from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, FileUploadView, RevenueSourceTotalsView

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('totals/', RevenueSourceTotalsView.as_view(), name='totals'),

]