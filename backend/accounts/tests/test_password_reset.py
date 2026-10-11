from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import PASSWORD, create_user, link_params

NEW_PASSWORD = 'a-completely-different-one'


@override_settings(EMAIL_ENABLED=True)
class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.post('/api/auth/password-reset/', {'email': self.user.email}, format='json')
        self.uid, self.token = link_params()

    def test_requesting_a_reset_emails_a_link(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Reset', mail.outbox[0].subject)

    def test_an_unknown_email_is_answered_identically_and_sends_nothing(self):
        before = len(mail.outbox)

        response = self.client.post('/api/auth/password-reset/', {'email': 'nobody@example.com'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(mail.outbox), before)

    @override_settings(EMAIL_ENABLED=False)
    def test_without_email_a_reset_asks_people_to_contact_support(self):
        before = len(mail.outbox)

        response = self.client.post('/api/auth/password-reset/', {'email': self.user.email}, format='json')

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn('contact support', response.data['detail'])
        self.assertEqual(len(mail.outbox), before)

    def test_the_link_sets_a_new_password(self):
        response = self.client.post(
            '/api/auth/password-reset/confirm/',
            {'uid': self.uid, 'token': self.token, 'password': NEW_PASSWORD},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        signed_in = self.client.post(
            '/api/auth/sign-in/', {'email': self.user.email, 'password': NEW_PASSWORD}, format='json'
        )
        self.assertEqual(signed_in.status_code, status.HTTP_200_OK)

    def test_the_old_password_stops_working(self):
        self.client.post(
            '/api/auth/password-reset/confirm/',
            {'uid': self.uid, 'token': self.token, 'password': NEW_PASSWORD},
            format='json',
        )

        response = self.client.post(
            '/api/auth/sign-in/', {'email': self.user.email, 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_the_link_cannot_be_used_twice(self):
        payload = {'uid': self.uid, 'token': self.token, 'password': NEW_PASSWORD}
        self.client.post('/api/auth/password-reset/confirm/', payload, format='json')

        response = self.client.post('/api/auth/password-reset/confirm/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_weak_new_password_is_rejected(self):
        response = self.client.post(
            '/api/auth/password-reset/confirm/',
            {'uid': self.uid, 'token': self.token, 'password': '123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(EMAIL_ENABLED=True)
class UnverifiedPasswordResetTests(APITestCase):
    def test_resetting_confirms_the_email_so_the_account_can_sign_in(self):
        user = create_user(email='unverified@example.com', verified=False)
        self.client.post('/api/auth/password-reset/', {'email': user.email}, format='json')
        uid, token = link_params()

        self.client.post(
            '/api/auth/password-reset/confirm/', {'uid': uid, 'token': token, 'password': NEW_PASSWORD}, format='json'
        )

        response = self.client.post(
            '/api/auth/sign-in/', {'email': user.email, 'password': NEW_PASSWORD}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
