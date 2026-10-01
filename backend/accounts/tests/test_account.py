from rest_framework import status
from rest_framework.test import APITestCase

from .factories import PASSWORD, create_user

NEW_PASSWORD = 'a-completely-different-one'


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.post('/api/auth/sign-in/', {'email': self.user.email, 'password': PASSWORD}, format='json')

    def test_the_name_can_be_changed(self):
        response = self.client.patch('/api/auth/me/', {'full_name': 'New Name'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'New Name')

    def test_the_email_cannot_be_changed_this_way(self):
        self.client.patch('/api/auth/me/', {'email': 'someone-else@example.com'}, format='json')

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'user@example.com')


class ChangePasswordTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.post('/api/auth/sign-in/', {'email': self.user.email, 'password': PASSWORD}, format='json')

    def change(self, current, new):
        return self.client.post(
            '/api/auth/change-password/', {'current_password': current, 'new_password': new}, format='json'
        )

    def test_changing_the_password_keeps_you_signed_in(self):
        response = self.change(PASSWORD, NEW_PASSWORD)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get('/api/auth/me/').status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(NEW_PASSWORD))

    def test_the_current_password_must_be_right(self):
        response = self.change('wrong', NEW_PASSWORD)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('current_password', response.data)

    def test_a_weak_new_password_is_rejected(self):
        response = self.change(PASSWORD, '123')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)

    def test_signed_out_requests_are_rejected(self):
        self.client.post('/api/auth/sign-out/')

        self.assertEqual(self.change(PASSWORD, NEW_PASSWORD).status_code, status.HTTP_401_UNAUTHORIZED)
