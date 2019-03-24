from rest_framework import serializers
from django.utils.text import slugify

# local imports
from questioner.apps.meetups.models import MeetUp, Tag
from questioner.apps.meetups.relations import TagsRelation
from questioner.apps.helpers.validators import Validators


class MeetUpSerializer(serializers.ModelSerializer):
    """
    serializers for meetup
    """
    user = serializers.SerializerMethodField(read_only=True)
    tags = TagsRelation(many=True, required=False)

    class Meta:
        model = MeetUp
        fields = (
            'user', 'slug', 'title', 'description', 'image_url', 'venue',
            'organizers', 'start_time', 'end_time', 'tags',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at', 'slug')

    def get_user(self, obj):
        return obj.user.username


class TagsSerializer(serializers.ModelSerializer):
    """
    serializers for Tags
    """
    class Meta:
        model = Tag
        fields = ('tag',)

    def create(self, validated_data):
        new_tag = validated_data['tag']
        Validators.string_has_no_special_characters(self, new_tag, 'Tag')
        tag, created = Tag.objects.get_or_create(tag=slugify(new_tag))
        return tag
