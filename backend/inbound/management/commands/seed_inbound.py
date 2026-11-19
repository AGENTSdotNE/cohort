import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from inbound.dates import parse_received
from inbound.models import InboundItem

SAMPLE_DATA = Path(__file__).resolve().parents[2] / 'sample_data.csv'


class Command(BaseCommand):
    help = 'Load the fictional inbound items from sample_data.csv.'

    def handle(self, *args, **options):
        with SAMPLE_DATA.open(newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                InboundItem.objects.update_or_create(
                    reference=row['ref'],
                    defaults={
                        'received_raw': row['received'],
                        'received_at': parse_received(row['received']),
                        'channel': row['channel'],
                        'sender': row['from'],
                        'subject': row['subject'],
                        'message': row['message'],
                        'logged_by': row['logged_by'],
                    },
                )

        self.stdout.write(f'{InboundItem.objects.count()} inbound items loaded.')
