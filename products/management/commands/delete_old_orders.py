from django.core.management.base import BaseCommand

from products.cron import delete_orders_unpaid_24_hours

class Command(BaseCommand):
    help = 'It deletes all orders in pending state with more than 24 hours old'

    def handle(self, *args, **options):
        delete_orders_unpaid_24_hours()
