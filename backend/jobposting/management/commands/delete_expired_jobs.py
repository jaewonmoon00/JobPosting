from django.core.management.base import BaseCommand
from django.db.models.functions import Now
from datetime import timedelta
from jobposting.models import Job

# a command that deletes jobs more than 90 days old, currently runnable thorugh command line, but can be done automatically with a service like celery
class Command(BaseCommand):
    def handle(self, *args, **options):
        Job.objects.filter(created_at__lte=Now()-timedelta(days=90)).delete()