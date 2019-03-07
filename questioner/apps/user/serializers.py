from rest_framework import serializers, status
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

# local imports
from questioner.apps.user.models import User, Profile
from questioner.apps.helpers.validators import Validators


class RegisterSerializer(serializers.ModelSerializer, Validators):
    """
    Serializer to validate user data during registration
    """

    def validate_username(self, data):
        return self.is_valid_string(data, 'Username')

    def validate_password(self, data):
        return self.is_valid_password(data)

    def validate(self, data):
        confirm_password = data.get('confirm_password', None)
        if data['password'] != confirm_password:
            raise serializers.ValidationError(
                "Password and confirm password don't match."
            )
        return data

    access_token = serializers.CharField(max_length=500, read_only=True)
    confirm_password = serializers.CharField(max_length=60, required=False)
    password = serializers.CharField(
        max_length=60, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name',
                  'password', 'access_token', 'confirm_password']

    def create(self, validated_data):
        # Use the `create_user` create a new user.
        validated_data.pop('confirm_password', None)
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=500, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed(
                'Invalid email or password', status.HTTP_401_UNAUTHORIZED)

        user_detail = {
            'full_name': user.full_name,
            'email': user.email,
            'username': user.username,
            'access_token': user.token
        }
        return user_detail


class GetProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile
    """
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = Profile
        fields = (
            'username', 'bio', 'image_url', 'company', 'phone', 'updated_at'
        )
        read_only_fields = ('updated_at',)
