from django.db import models
from django.conf import settings
from django.utils import timezone


class EmailOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_valid(self):
        return((not self.used) and (timezone.now()) <= self.expires_at)
    
    def mark_used(self):
        self.used = True
        self.save()

# Create your models here.
