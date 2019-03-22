from rest_framework import serializers

# local imports
from questioner.apps.questions.models import Questions


class QusetionSerializer(serializers.ModelSerializer):
    """
    serializers for questions
    """
    author = serializers.SerializerMethodField(read_only=True)
    meetup = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Questions
        fields = (
            'author', 'meetup', 'content', 'created_at', 'updated_at', 'id',
            'parent'
        )
        read_only_fields = ('created_at', 'updated_at', 'id')

    def get_author(self, obj):
        return obj.user.username

    def get_meetup(self, obj):
        return obj.meetup.title

    def to_representation(self, instance):
        """
        overide representation for custom output
        """
        threads = self.get_threads(instance)
        representation = super().to_representation(instance)
        representation['replies_count'] = instance.threads.count()
        representation['threads'] = threads
        del representation['parent']

        return representation

    def get_threads(self, question):
        # recurcively get threaded questions
        threads = []
        for thread in question.threads.all():
            reply = {
                'author': thread.user.username,
                'meetup': thread.meetup.title,
                'content': thread.content,
                'created_at': thread.created_at,
                'updated_at': thread.updated_at,
                'id': thread.id,
                'replies_count': thread.threads.count()
            }
            threads.append(reply)
            if thread.threads.count() > 0:
                reply['threads'] = self.get_threads(thread)
            else:
                reply['thread'] = []
        return threads
