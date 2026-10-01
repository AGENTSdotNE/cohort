import re
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

User = get_user_model()

PASSWORD = 'correct-horse-battery'


def create_user(email='user@example.com', verified=True, **extra):
    return User.objects.create_user(email=email, password=PASSWORD, email_verified=verified, **extra)


def link_params():
    return re.search(r'uid=([\w\-]+)&token=([\w\-]+)', mail.outbox[-1].body).groups()


def image_upload(name='me.png'):
    buffer = BytesIO()
    Image.new('RGB', (8, 8)).save(buffer, 'PNG')

    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')
