import getpass
import re
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Used to create admin.'
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()
        self.users_query = self.UserModel.objects.all()

    def handle(self, *args, **options):
        full_name = self.get_full_name()
        email = self.get_email()
        username = self.get_username()
        password = self.get_password()
        self.UserModel.objects.create_admin(
            full_name, username, email, password)
        self.stdout.write("Superuser created successfully.")

    def get_input_data(self, field, message):
        """
        Prompt admin to input details
        """
        raw_value = input(message)
        return raw_value

    def validate_password(self, password):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).*', password):  # noqa E501
            return False
        return True

    def validate_email(self, email):
        valid = re.match(
            "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip()) # noqa E501
        if valid is None:
            return False
        return True

    def validate_string(self, string):
        valid = re.match("(^[a-zA-Z]+)", string)
        if valid is None:
            return False
        return True

    def get_full_name(self):
        full_name_valid = False
        while not full_name_valid:
            full_name = self.get_input_data('full_name', 'Full Name : ')
            if not self.validate_string(full_name):
                self.stderr.write(
                    "Error: Full name can only contain character only")
                continue
            full_name_valid = True
            return full_name

    def get_username(self):
        username_exist = False
        while not username_exist:
            username = self.get_input_data('username', 'Username : ')
            if self.users_query.filter(username=username):
                self.stderr.write("Error: Username already taken")
                continue
            username_exist = True
            return username

    def get_email(self):
        email_valid = False
        while not email_valid:
            email = self.get_input_data('email', 'Email : ')
            if not self.validate_email(email):
                self.stderr.write("Error: Invalid email")
                continue
            if self.users_query.filter(email=email):
                self.stderr.write("Error: Email already taken")
                continue
            email_valid = True
            return email

    def get_password(self):
        pass_match_valid = False
        while not pass_match_valid:
            password = getpass.getpass()
            confirm_password = getpass.getpass('Password (again): ')
            if password != confirm_password:
                self.stderr.write("Error: Your passwords didn't match.")
                continue
            if not self.validate_password(password):
                self.stderr.write(
                    "Error: Password must contain a number, capital letter and special charachter")  # noqa E501
                continue
            pass_match_valid = True
            return password
