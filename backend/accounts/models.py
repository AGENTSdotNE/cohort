"""The project's user model: email is the login, there is no separate username."""

import uuid
from pathlib import Path

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


def avatar_upload_path(user, filename):
    # A random name keeps the uploader's filename private and gives each new picture a fresh URL.
    return f'avatars/{uuid.uuid4().hex}{Path(filename).suffix.lower()}'


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('email_verified', True)

        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Stored lowercase so the unique constraint, and every iexact lookup, agree on one address per account.
        self.email = self.email.lower()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email


# A signal rather than an overridden delete(), because admin's bulk delete never calls delete() on each user.
@receiver(post_delete, sender=User)
def delete_avatar_file(sender, instance, **kwargs):
    instance.avatar.delete(save=False)
