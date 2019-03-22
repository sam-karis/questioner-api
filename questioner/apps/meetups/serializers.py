from rest_framework import serializers
# local imports
from questioner.apps.meetups.models import MeetUp


class MeetUpSerializer(serializers.ModelSerializer):
    """
    serializers for meetup
    """
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MeetUp
        fields = (
            'user', 'slug', 'title', 'description', 'image_url', 'venue',
            'organizers', 'start_time', 'end_time',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at', 'slug')

    def get_user(self, obj):
        return obj.user.username
