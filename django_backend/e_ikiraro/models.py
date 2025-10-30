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
        ('Emergency Travel Document', 'Approved'),
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True, related_name='passport_details')
    passport_type = models.CharField(max_length=500, choices=PASSPORT_TYPES)
    national_id = models.CharField(max_length=20, blank = True)

    def __str__(self):
        return f"Passport Application for {self.application.user.username}"


class NationalIDApplication(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True, related_name='national_id_details')
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f'National ID Application for {self.application.user.username}'
    

class DriversLicenseApplication(models.Model):
    pass
    # LICESCENSE_TYPES = [


    # application = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True, related_name='drivers_license_details')



class Payment(models.Model):
    pass

class Document(models.Model):
    pass









