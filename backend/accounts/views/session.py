from django.conf import settings
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import ProfileSerializer, SignInSerializer, UserSerializer


@method_decorator(ensure_csrf_cookie, name='get')
class CsrfView(APIView):
    """The frontend calls this once on boot to receive the CSRF cookie."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthConfigView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'email_enabled': settings.EMAIL_ENABLED})


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return Response(UserSerializer(user).data)


class SignOutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserSerializer(request.user).data)
