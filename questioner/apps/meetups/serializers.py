from rest_framework import serializers
# local imports
from questioner.apps.meetups.models import MeetUp


class MeetUpSerializer(serializers.ModelSerializer):
    """
    serializers for meetup
    """

    class Meta:
        model = MeetUp
        fields = (
            'user', 'id', 'title', 'description', 'image_url', 'venue',
            'organizers', 'start_time', 'end_time',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at', 'user', 'id')
