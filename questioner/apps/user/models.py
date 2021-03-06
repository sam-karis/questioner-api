from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin
)
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime as date_time, timedelta
import jwt


class CustomUserManager(UserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, full_name, username, email, password=None, **extra_fields):  # noqa E501
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        extra_fields.setdefault('full_name', full_name)
        user = self._create_user(username, email, password, **extra_fields)

        return user

    def create_admin(self, full_name, username, email, password, **extra_fields):  # noqa E501
        """Create and return a `User` with an email, username and password."""
        extra_fields.setdefault('full_name', full_name)
        extra_fields.setdefault('is_staff', True)
        user = self._create_user(username, email, password, **extra_fields)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # User full name
    full_name = models.CharField(max_length=255)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # When a user is created this field is false until the user verifies their
    # identity
    is_verified = models.BooleanField(default=False)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # false
    is_staff = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = CustomUserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.username

    @property
    def token(self):
        """
        This method allows us to get the token by calling 'user.token'
        """
        return self.generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name.
        """
        return self.full_name

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name.
        """
        return self.username

    def generate_jwt_token(self):
        """This method generates a JSON Web Token """
        user_details = {'email': self.email,
                        'username': self.username,
                        'full_name': self.full_name}
        token = jwt.encode(
            {
                'user_data': user_details,
                'exp': date_time.now() + timedelta(days=7)
            }, settings.SECRET_KEY, algorithm='HS256'
        )
        return token.decode('utf-8')


class Profile(models.Model):
    """
    create a user profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image_url = models.CharField(max_length=500, null=True)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    create profile upon user registration.
    """
    Profile.objects.create(user=instance)
    instance.profile.save()
