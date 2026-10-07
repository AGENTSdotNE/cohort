from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import PASSWORD, create_user, link_params


class SignUpTests(APITestCase):
    def test_sign_up_creates_an_unverified_account_and_sends_one_email(self):
        response = self.client.post(
            '/api/auth/sign-up/',
            {'email': 'new@example.com', 'full_name': 'New User', 'password': PASSWORD},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['email_verified'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Confirm', mail.outbox[0].subject)

    def test_a_weak_password_is_rejected(self):
        response = self.client.post(
            '/api/auth/sign-up/', {'email': 'weak@example.com', 'password': '123'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_a_duplicate_email_is_rejected(self):
        create_user(email='taken@example.com')

        response = self.client.post(
            '/api/auth/sign-up/', {'email': 'taken@example.com', 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_the_password_is_never_returned(self):
        response = self.client.post(
            '/api/auth/sign-up/', {'email': 'new@example.com', 'password': PASSWORD}, format='json'
        )

        self.assertNotIn('password', response.data)

    def test_the_account_is_not_kept_if_the_email_cannot_be_sent(self):
        with (
            patch('accounts.views.registration.send_verification_email', side_effect=ConnectionError),
            self.assertRaises(ConnectionError),
        ):
            self.client.post('/api/auth/sign-up/', {'email': 'new@example.com', 'password': PASSWORD}, format='json')

        self.assertFalse(get_user_model().objects.filter(email='new@example.com').exists())

    @override_settings(EMAIL_ENABLED=False)
    def test_without_email_the_account_is_signed_in_with_no_email(self):
        response = self.client.post(
            '/api/auth/sign-up/', {'email': 'new@example.com', 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['email_verified'])
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(self.client.get('/api/auth/me/').status_code, status.HTTP_200_OK)


class VerifyEmailTests(APITestCase):
    def setUp(self):
        self.client.post('/api/auth/sign-up/', {'email': 'new@example.com', 'password': PASSWORD}, format='json')
        self.uid, self.token = link_params()

    def test_the_emailed_link_verifies_the_account_and_sends_a_welcome(self):
        response = self.client.post('/api/auth/verify-email/', {'uid': self.uid, 'token': self.token}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['email_verified'])
        self.assertIn('Welcome', mail.outbox[-1].subject)

    def test_the_link_stops_working_once_it_has_been_used(self):
        self.client.post('/api/auth/verify-email/', {'uid': self.uid, 'token': self.token}, format='json')

        response = self.client.post('/api/auth/verify-email/', {'uid': self.uid, 'token': self.token}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_tampered_token_is_rejected(self):
        response = self.client.post(
            '/api/auth/verify-email/', {'uid': self.uid, 'token': 'not-the-token'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resending_verification_does_not_reveal_whether_the_account_exists(self):
        unknown = self.client.post('/api/auth/resend-verification/', {'email': 'nobody@example.com'}, format='json')
        known = self.client.post('/api/auth/resend-verification/', {'email': 'new@example.com'}, format='json')

        self.assertEqual(unknown.status_code, known.status_code)

    @override_settings(EMAIL_ENABLED=False)
    def test_without_email_resending_says_you_can_sign_in_anyway(self):
        before = len(mail.outbox)

        response = self.client.post('/api/auth/resend-verification/', {'email': 'new@example.com'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn('sign in without confirming', response.data['detail'])
        self.assertEqual(len(mail.outbox), before)
