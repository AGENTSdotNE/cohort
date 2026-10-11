from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings

from accounts.management.commands.seed import PASSWORD, USERS
from accounts.models import User


@override_settings(DEBUG=True)
class SeedTests(TestCase):
    def test_creates_confirmed_accounts_that_can_sign_in(self):
        call_command('seed', stdout=StringIO())

        self.assertEqual(User.objects.count(), len(USERS))
        for user in User.objects.all():
            self.assertTrue(user.email_verified)
            self.assertTrue(self.client.login(username=user.email, password=PASSWORD))

    def test_running_twice_does_not_duplicate_accounts(self):
        call_command('seed', stdout=StringIO())
        call_command('seed', stdout=StringIO())

        self.assertEqual(User.objects.count(), len(USERS))

    @override_settings(DEBUG=False)
    def test_refuses_to_run_with_debug_off(self):
        with self.assertRaises(CommandError):
            call_command('seed', stdout=StringIO())

        self.assertFalse(User.objects.exists())
