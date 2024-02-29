from django.db import models


class Invoice(models.Model):
    invoice_number = models.IntegerField()
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
        indexes = [
            models.Index(fields=['revenue_source']),
        ]
        constraints = [
            models.UniqueConstraint(name='unique_invoice_number_customer', fields=['invoice_number', 'customer'])
        ]

