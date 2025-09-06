from django.core.management.base import BaseCommand
from tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Unblock an IP address by removing it from the BlockedIP list."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="The IP address to unblock")

    def handle(self, *args, **options):
        ip = options["ip_address"]
        deleted, _ = BlockedIP.objects.filter(ip_address=ip).delete()
        if deleted:
            self.stdout.write(self.style.SUCCESS(f"Seccessfully unblocked IP: {ip}"))
        else:
            self.stdout.write(self.style.WARNING(f"IP address {ip} was not found in the block list."))

