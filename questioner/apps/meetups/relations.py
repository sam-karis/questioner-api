from rest_framework import serializers
from django.utils.text import slugify

from questioner.apps.meetups.models import Tag
from questioner.apps.helpers.validators import Validators


class TagsRelation(serializers.RelatedField):

    queryset = Tag.objects.all()

    def to_representation(self, value):
        return value.tag

    def to_internal_value(self, data):
        Validators.string_has_no_special_characters(self, data, 'Tag')
        tag, created = Tag.objects.get_or_create(tag=slugify(data))
        return tag
