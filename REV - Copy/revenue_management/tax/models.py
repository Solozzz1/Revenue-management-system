from django.db import models
from django.conf import settings

# Tax Type Model
class TaxType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Bill Type Model
class BillType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Tax Invoice Model
class TaxInvoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    tax_type = models.ForeignKey(TaxType, on_delete=models.CASCADE)
    bill_type = models.ForeignKey(BillType, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status_choices = [
        ('P', 'Paid'),
        ('U', 'Unpaid'),
        ('O', 'Overdue'),
        ('PP', 'Partially Paid'),
    ]
    status = models.CharField(max_length=2, choices=status_choices, default='U')

    def __str__(self):
        return f"Invoice {self.id} for {self.user}"

# Payment Model
class Payment(models.Model):
    invoice = models.ForeignKey(TaxInvoice, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=255)
    payment_method_choices = [
        ('CC', 'Credit Card'),
        ('BT', 'Bank Transfer'),
        ('PP', 'PayPal'),
        ('MP', 'Mobile Payment'),
    ]
    payment_method = models.CharField(max_length=2, choices=payment_method_choices)

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.id}"

# Taxpayer Category Model
class TaxpayerCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, unique=True, blank=False)
    physical_address = models.TextField(blank=False)
    email = models.EmailField(unique=True, blank=False)
    country = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_registration_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    income_range = models.CharField(max_length=50, blank=True, null=True, default='Unspecified')
    taxpayer_category = models.ForeignKey(TaxpayerCategory, on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.id_number if self.id_number else self.business_name}"
