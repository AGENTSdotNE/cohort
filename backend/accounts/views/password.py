from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..emails import send_password_reset_email
from ..serializers import ChangePasswordSerializer, EmailSerializer, PasswordResetConfirmSerializer

User = get_user_model()


class PasswordResetView(APIView):
    """Always answers the same way, so the response cannot be used to discover who has an account."""

    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.EMAIL_ENABLED:
            return Response(
                {'detail': 'Password reset by email is not available yet. Please contact support.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=serializer.validated_data['email'], is_active=True).first()

        if user is not None:
            send_password_reset_email(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        # Following the emailed link proves they own the address, so they should not be locked out of sign-in.
        user.email_verified = True
        user.save(update_fields=['password', 'email_verified'])

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        # Changing the password signs out every session, so re-issue this one to keep the person signed in here.
        update_session_auth_hash(request, request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
