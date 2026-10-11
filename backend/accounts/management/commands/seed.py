"""Creates fictional, already-confirmed accounts for trying the app and testing permissions."""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from accounts.models import User

PASSWORD = 'cohort-dev-password'

USERS = [
    {'email': 'alex@example.com', 'full_name': 'Alex Example'},
    {'email': 'sam@example.com', 'full_name': 'Sam Example'},
    {'email': 'staff@example.com', 'full_name': 'Staff Example', 'is_staff': True, 'is_superuser': True},
]


class Command(BaseCommand):
    help = 'Create fictional accounts that can sign in straight away. Development only.'

    def handle(self, *args, **options):
        # Everyone knows this password, so these accounts must never exist on a shared server.
        if not settings.DEBUG:
            raise CommandError('seed only runs with DEBUG on.')

        for fields in USERS:
            if User.objects.filter(email=fields['email']).exists():
                self.stdout.write(f'{fields["email"]} already exists')
                continue

            User.objects.create_user(password=PASSWORD, email_verified=True, **fields)
            self.stdout.write(f'Created {fields["email"]}')

        self.stdout.write(f'Every account uses the password "{PASSWORD}".')
