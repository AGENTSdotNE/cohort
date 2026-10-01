from html import unescape

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from .tokens import email_verification_token


def send_templated_email(to, subject, template, context):
    html = render_to_string(f'emails/{template}.html', {**context, 'subject': subject})
    message = EmailMultiAlternatives(subject, _plain_text(html), settings.DEFAULT_FROM_EMAIL, [to])
    message.attach_alternative(html, 'text/html')
    message.send()


def _plain_text(html):
    # Unescaping turns &amp; back into &, otherwise links in the plain text half would be broken.
    lines = (line.strip() for line in unescape(strip_tags(html)).splitlines())

    return '\n\n'.join(line for line in lines if line)


def _link(path, user, token):
    return f'{settings.FRONTEND_URL}/{path}?uid={urlsafe_base64_encode(force_bytes(user.pk))}&token={token}'


def send_verification_email(user):
    send_templated_email(
        user.email,
        f'Confirm your {settings.SITE_NAME} email address',
        'verify_email',
        {'user': user, 'link': _link('verify-email', user, email_verification_token.make_token(user))},
    )


def send_welcome_email(user):
    send_templated_email(
        user.email, f'Welcome to {settings.SITE_NAME}', 'welcome', {'user': user, 'link': settings.FRONTEND_URL}
    )


def send_password_reset_email(user):
    send_templated_email(
        user.email,
        f'Reset your {settings.SITE_NAME} password',
        'password_reset',
        {
            'user': user,
            'link': _link('reset-password', user, default_token_generator.make_token(user)),
            'timeout_hours': settings.PASSWORD_RESET_TIMEOUT // 3600,
        },
    )
