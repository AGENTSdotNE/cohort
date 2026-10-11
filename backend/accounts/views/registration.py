from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..emails import send_verification_email, send_welcome_email
from ..serializers import EmailSerializer, SignUpSerializer, UserSerializer, VerifyEmailSerializer

User = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]

    # If the email cannot be sent the account is rolled back, so the person can simply try again.
    @transaction.atomic
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if settings.EMAIL_ENABLED:
            send_verification_email(user)
        else:
            # Nothing to confirm with, and it stops them being locked out if email is switched on later.
            user.email_verified = True
            user.save(update_fields=['email_verified'])
            login(request, user)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.email_verified:
            user.email_verified = True
            user.save(update_fields=['email_verified'])
            send_welcome_email(user)

        return Response(UserSerializer(user).data)


class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.EMAIL_ENABLED:
            return Response(
                {'detail': 'Confirmation emails are not available yet. You can sign in without confirming.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=serializer.validated_data['email'], email_verified=False).first()

        if user is not None:
            send_verification_email(user)

        return Response(status=status.HTTP_204_NO_CONTENT)
