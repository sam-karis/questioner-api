import re
from rest_framework import serializers


class Validators(object):

    def is_valid_password(self, password):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).*', password):  # noqa E501
            raise serializers.ValidationError(
                'Password must contain a number, capital letter and special charachter'  # noqa E501
            )
        return password

    def is_valid_string(self, string, entity):
        if re.match(r'^[0-9]+[A-Za-z0-9]]*$', string):
            raise serializers.ValidationError(
                f'{entity} cannot contain numbers or special characters only'
            )
        return string

    def string_has_no_special_characters(self, string, entity):
        if not re.match(r'^[a-zA-Z0-9][ A-Za-z0-9_-]*$', string):
            raise serializers.ValidationError(
                f'{entity} cannot have special characters')
