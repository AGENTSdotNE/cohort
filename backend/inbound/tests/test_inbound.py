from datetime import UTC, datetime
from io import StringIO

from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.factories import create_user

from ..models import InboundItem

URL = '/api/inbound/'


def create_item(reference, received_at=None, **extra):
    return InboundItem.objects.create(reference=reference, received_at=received_at, channel='email', **extra)


class InboundListTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_a_row_has_everything_the_list_shows(self):
        create_item(
            'EM-1',
            received_at=datetime(2026, 9, 3, 9, 14, tzinfo=UTC),
            received_raw='03/09/2026 09:14',
            sender='sam@example.com',
            subject='Fly-tipping',
            message='How many fines?',
        )

        response = self.client.get(URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data[0]),
            {'id', 'reference', 'received_raw', 'received_at', 'channel', 'sender', 'subject', 'message', 'logged_by'},
        )
        self.assertEqual(response.data[0]['received_at'], '2026-09-03T10:14:00+01:00')

    def test_unknown_dates_come_first_then_newest(self):
        create_item('OLD', received_at=datetime(2026, 9, 1, tzinfo=UTC))
        create_item('NEW', received_at=datetime(2026, 10, 1, tzinfo=UTC))
        create_item('UNKNOWN', received_raw='22/9')

        response = self.client.get(URL)

        self.assertEqual([item['reference'] for item in response.data], ['UNKNOWN', 'NEW', 'OLD'])
        self.assertIsNone(response.data[0]['received_at'])

    def test_every_officer_sees_the_same_items(self):
        create_item('EM-1')
        create_item('PH-2')
        mine = self.client.get(URL).data

        self.client.force_authenticate(create_user(email='other@example.com'))
        theirs = self.client.get(URL).data

        self.assertEqual(len(mine), 2)
        self.assertEqual(mine, theirs)

    def test_empty_database_gives_an_empty_list(self):
        response = self.client.get(URL)

        self.assertEqual(response.data, [])

    def test_signed_out_gets_401(self):
        self.client.force_authenticate(None)

        response = self.client.get(URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_items_cannot_be_changed_through_the_api(self):
        item = create_item('EM-1')

        self.assertEqual(self.client.post(URL, {'reference': 'X'}).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            self.client.patch(f'{URL}{item.id}/', {'subject': 'X'}).status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(self.client.delete(f'{URL}{item.id}/').status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SeedInboundTests(APITestCase):
    def test_loads_all_eight_sample_items_and_can_run_twice(self):
        call_command('seed_inbound', stdout=StringIO())
        call_command('seed_inbound', stdout=StringIO())

        self.assertEqual(InboundItem.objects.count(), 8)

    def test_unreadable_date_is_stored_without_guessing(self):
        call_command('seed_inbound', stdout=StringIO())

        phone_note = InboundItem.objects.get(reference='PH-0093')

        self.assertIsNone(phone_note.received_at)
        self.assertEqual(phone_note.received_raw, '22/9')
        self.assertEqual(phone_note.sender, '')
