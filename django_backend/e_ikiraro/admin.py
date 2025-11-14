from django.contrib import admin
from .models import Service, PassportApplication, NationalIDApplication, DriversLicenseApplication,Payment, Document


# Register your models here.

admin.site.register(Service)
admin.site.register(PassportApplication)
admin.site.register(NationalIDApplication)
admin.site.register(DriversLicenseApplication)
admin.site.register(Payment)
admin.site.register(Document)
