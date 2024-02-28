from django.utils import timezone
from django.db import models

# TODO: It is has some sense to add this base class?
# class BaseModel(models.Model):
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

# class Meta:
#         abstract = True

class Invoice(models.Model):
    invoice_number = models.IntegerField(primary_key=True, unique=True)
    date = models.DateField()
    customer = models.CharField(max_length=100)
    revenue_source = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    haircut_percent = models.IntegerField()
    daily_fee_percent = models.DecimalField(max_digits=7, decimal_places=3)
    currency = models.CharField(max_length=3)
    expected_payment_duration = models.IntegerField()

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer} - {self.date}"

    class Meta:
        ordering = ['-date']


class UploadedFile(models.Model):
    file = models.FileField(upload_to='data/')
    uploaded_at = models.DateTimeField(auto_now_add=True)