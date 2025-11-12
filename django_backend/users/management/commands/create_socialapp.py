from django.core.management.base import BaseCommand
from decouple import config
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Create/update Google SocialApp from environment variables"

    def handle(self, *args, **options):
        client_id = config('GOOGLE_CLIENT_ID', default='')
        secret = config('GOOGLE_CLIENT_SECRET', default='')
        if not client_id or not secret:
            self.stderr.write(
                "GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set in environment")
            return
        site = Site.objects.get(pk=1)
        app, created = SocialApp.objects.update_or_create(
            provider='google',
            defaults={'name': 'Google',
                      'client_id': client_id, 'secret': secret},
        )
        app.sites.set([site])
        app.save()
        self.stdout.write(self.style.SUCCESS(
            "SocialApp for Google created/updated"))
