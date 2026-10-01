"""Signed, expiring links for email verification."""

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Including email_verified means a link stops working the moment it has been used."""

    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{timestamp}{user.email_verified}{user.email}'


email_verification_token = EmailVerificationTokenGenerator()
