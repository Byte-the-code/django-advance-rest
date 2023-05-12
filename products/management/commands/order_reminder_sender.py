from django.core.management.base import BaseCommand

from products.cron import order_reminder_sender

class Command(BaseCommand):
    help = "It sends an email to remind all users that have and ortder in pending state with less than 24 hs to complete it"

    def handle(self, *args, **options):
        order_reminder_sender()
