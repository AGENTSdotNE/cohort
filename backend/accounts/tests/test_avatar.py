import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import create_user, image_upload

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class AvatarTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.addClassCleanup(shutil.rmtree, MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def upload(self, file):
        return self.client.put('/api/auth/me/avatar/', {'avatar': file}, format='multipart')

    def stored_file(self):
        self.user.refresh_from_db()

        return Path(self.user.avatar.path)

    def test_uploading_a_picture_returns_its_url(self):
        response = self.upload(image_upload())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['avatar_url'].startswith('/media/avatars/'))
        self.assertTrue(self.stored_file().exists())

    def test_a_file_that_is_not_an_image_is_rejected(self):
        response = self.upload(SimpleUploadedFile('me.png', b'not really a picture', content_type='image/png'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('avatar', response.data)

    def test_a_picture_over_the_size_limit_is_rejected(self):
        with patch('accounts.serializers.MAX_AVATAR_BYTES', 10):
            response = self.upload(image_upload())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('2 MB', str(response.data['avatar']))

    def test_replacing_a_picture_deletes_the_old_file(self):
        self.upload(image_upload())
        old = self.stored_file()

        self.upload(image_upload())

        self.assertFalse(old.exists())
        self.assertTrue(self.stored_file().exists())

    def test_removing_the_picture_deletes_the_file(self):
        self.upload(image_upload())
        old = self.stored_file()

        response = self.client.delete('/api/auth/me/avatar/')

        self.assertIsNone(response.data['avatar_url'])
        self.assertFalse(old.exists())

    def test_deleting_the_user_deletes_their_picture(self):
        self.upload(image_upload())
        old = self.stored_file()

        self.user.delete()

        self.assertFalse(old.exists())

    def test_signed_out_uploads_are_rejected(self):
        self.client.force_authenticate(None)

        self.assertEqual(self.upload(image_upload()).status_code, status.HTTP_401_UNAUTHORIZED)
