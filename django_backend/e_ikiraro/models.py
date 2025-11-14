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


class PassportApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending submission'),
        ('Submitted', 'Submitted'),
        ('Processing', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    PASSPORT_TYPES = [
        ('Ordinary Passport', 'Ordinary Passport'),
        ('Official Passport', 'Official Passport'),
        ('Diplomatic Passport', 'Diplomatic Passport'),
        ('Emergency Travel Document', 'Emergency Travel Document'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passport_applications', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, null=True, blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    current_address = models.TextField(null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    previous_passport_number = models.CharField(max_length=50, blank=True)
    previous_passport_issue_date = models.DateField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    passport_type = models.CharField(max_length=500, choices=PASSPORT_TYPES)
    passport_photo = models.FileField(upload_to='documents/passport_photos/')
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/')
    national_id = models.FileField(upload_to='documents/national_ids/')

    def __str__(self):
        return f"Passport Application for {self.user.username}"


class NationalIDApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending submission'),
        ('Submitted', 'Submitted'),
        ('Processing', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='national_id_applications', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/')
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f'National ID Application for {self.user.username}'


class DriversLicenseApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending submission'),
        ('Submitted', 'Submitted'),
        ('Processing', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    LICENSE_TYPES = [
        ('Motorcycle', 'Motorcycle'),
        ('Personal Car', 'Personal Car'),
        ('Commercial Vehicle', 'Commercial Vehicle'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drivers_license_applications', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    license_type = models.CharField(max_length=50, choices=LICENSE_TYPES)
    photo = models.FileField(upload_to='documents/license_photos/')
    medical_certificate = models.FileField(upload_to='documents/medical_certificates/')
    eye_test_certificate = models.FileField(upload_to='documents/eye_test_certificates/')
    national_id = models.FileField(upload_to='documents/national_ids/')
    driving_school_certificate = models.FileField(upload_to='documents/driving_school_certificates/', blank=True, default='')
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Driver's License Application for {self.user.username}"


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
    
    passport_application = models.ForeignKey(PassportApplication, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    national_id_application = models.ForeignKey(NationalIDApplication, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    drivers_license_application = models.ForeignKey(DriversLicenseApplication, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
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
    
    # Generic content type fields to link to any application type
    passport_application = models.ForeignKey(PassportApplication, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    national_id_application = models.ForeignKey(NationalIDApplication, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    drivers_license_application = models.ForeignKey(DriversLicenseApplication, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.document_type} for {self.user.username}"









