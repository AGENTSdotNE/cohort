from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .tokens import email_verification_token

User = get_user_model()


def _user_from_uid(uid):
    try:
        return User.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


MAX_AVATAR_BYTES = 2 * 1024 * 1024


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'email_verified', 'avatar_url']
        read_only_fields = fields

    def get_avatar_url(self, user):
        return user.avatar.url if user.avatar else None


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name']


class AvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField()

    def validate_avatar(self, value):
        if value.size > MAX_AVATAR_BYTES:
            raise serializers.ValidationError('Choose an image smaller than 2 MB.')

        return value


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                lookup='iexact',
                message='An account with this email address already exists.',
            )
        ]
    )
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(self.context['request'], username=attrs['email'], password=attrs['password'])

        if user is None:
            raise serializers.ValidationError('Your email address or password is incorrect.')

        if not user.email_verified:
            raise serializers.ValidationError('Confirm your email address before signing in.')

        attrs['user'] = user

        return attrs


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class TokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    token_generator = default_token_generator

    def validate(self, attrs):
        user = _user_from_uid(attrs['uid'])

        if user is None or not self.token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('This link is invalid or has expired.')

        attrs['user'] = user

        return attrs


class VerifyEmailSerializer(TokenSerializer):
    token_generator = email_verification_token


class PasswordResetConfirmSerializer(TokenSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Your current password is incorrect.')

        return value

    def validate_new_password(self, value):
        validate_password(value, user=self.context['request'].user)

        return value
