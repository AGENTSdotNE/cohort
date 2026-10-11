from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import PASSWORD, create_user


class SessionTests(APITestCase):
    def setUp(self):
        self.user = create_user()

    def test_signing_in_returns_the_user_and_starts_a_session(self):
        response = self.client.post(
            '/api/auth/sign-in/', {'email': self.user.email, 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(self.client.get('/api/auth/me/').status_code, status.HTTP_200_OK)

    def test_the_email_is_matched_regardless_of_case(self):
        response = self.client.post(
            '/api/auth/sign-in/', {'email': 'USER@EXAMPLE.COM', 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_a_wrong_password_does_not_say_which_field_was_wrong(self):
        response = self.client.post(
            '/api/auth/sign-in/', {'email': self.user.email, 'password': 'wrong'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email address or password is incorrect', str(response.data))

    def test_an_unknown_account_gives_the_same_answer_as_a_wrong_password(self):
        wrong_password = self.client.post(
            '/api/auth/sign-in/', {'email': self.user.email, 'password': 'wrong'}, format='json'
        )
        unknown = self.client.post(
            '/api/auth/sign-in/', {'email': 'nobody@example.com', 'password': 'wrong'}, format='json'
        )

        self.assertEqual(str(wrong_password.data), str(unknown.data))

    @override_settings(EMAIL_ENABLED=True)
    def test_an_unverified_account_cannot_sign_in(self):
        create_user(email='unverified@example.com', verified=False)

        response = self.client.post(
            '/api/auth/sign-in/', {'email': 'unverified@example.com', 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Confirm your email address', str(response.data))

    @override_settings(EMAIL_ENABLED=False)
    def test_without_email_an_unverified_account_can_sign_in(self):
        create_user(email='unverified@example.com', verified=False)

        response = self.client.post(
            '/api/auth/sign-in/', {'email': 'unverified@example.com', 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_is_rejected_while_signed_out(self):
        self.assertEqual(self.client.get('/api/auth/me/').status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signing_out_ends_the_session(self):
        self.client.post('/api/auth/sign-in/', {'email': self.user.email, 'password': PASSWORD}, format='json')
        self.client.post('/api/auth/sign-out/')

        self.assertEqual(self.client.get('/api/auth/me/').status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(EMAIL_ENABLED=True)
    def test_the_config_says_email_is_on(self):
        response = self.client.get('/api/auth/config/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'email_enabled': True})

    @override_settings(EMAIL_ENABLED=False)
    def test_the_config_says_email_is_off_without_signing_in(self):
        response = self.client.get('/api/auth/config/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'email_enabled': False})

    def test_the_csrf_endpoint_sets_the_cookie(self):
        response = self.client.get('/api/auth/csrf/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('csrftoken', response.cookies)

    def test_an_address_stored_in_mixed_case_still_resolves_to_one_account(self):
        create_user(email='Mixed@Example.com', verified=True)

        response = self.client.post(
            '/api/auth/sign-in/', {'email': 'mixed@example.com', 'password': PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'mixed@example.com')
