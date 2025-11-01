import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, help_text="Name of the service")
    description = models.TextField(help_text="Description of the service")
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Base fee for the service")

    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending submission'),
        ('Submitted', 'Submitted'),
        ('Processing', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='applications', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f" {self.service.name} for {self.user.username}"


class PassportApplication(models.Model):
    PASSPORT_TYPES = [
        ('Ordinary Passport', 'Ordinary Passport'),
        ('Official Passport', 'Official Passport'),
        ('Diplomatic Passport', 'Diplomatic Passport'),
        ('Emergency Travel Document', 'Emergency Travel Document'),
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True, related_name='passport_details')
    passport_type = models.CharField(max_length=500, choices=PASSPORT_TYPES)
    passport_photo = models.FileField(upload_to='documents/passport_photos/')
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/')
    national_id = models.FileField(upload_to='documents/national_ids/')

    def __str__(self):
        return f"Passport Application for {self.application.user.username}"


class NationalIDApplication(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True, related_name='national_id_details')
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/')
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f'National ID Application for {self.application.user.username}'
    

class DriversLicenseApplication(models.Model):
    LICENSE_TYPES = [
        ('Motorcycle', 'Motorcycle'),
        ('Personal Car', 'Personal Car'),
        ('Commercial Vehicle', 'Commercial Vehicle'),
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True, related_name='drivers_license_details')
    license_type = models.CharField(max_length=50, choices=LICENSE_TYPES)
    photo = models.FileField(upload_to='documents/license_photos/')
    medical_certificate = models.FileField(upload_to='documents/medical_certificates/')
    eye_test_certificate = models.FileField(upload_to='documents/eye_test_certificates/')
    national_id = models.FileField(upload_to='documents/national_ids/')

    def __str__(self):
        return f"Driver's License Application for {self.application.user.username}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Mobile Money', 'Mobile Money'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='payments')
    service_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100)
    provider_reference = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    paid_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} for {self.service_type}"


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('Passport', 'Passport'),
        ('National ID', 'National ID'),
        ('Driver License', 'Driver License'),
        ('Birth Certificate', 'Birth Certificate'),
        ('Medical Certificate', 'Medical Certificate'),
        ('Other', 'Other'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.document_type} for {self.application.user.username}"









