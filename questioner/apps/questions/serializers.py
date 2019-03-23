from rest_framework import serializers
from rest_framework.validators import ValidationError


# local imports
from questioner.apps.questions.models import Questions, Votes


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


class VotesSerializer(serializers.ModelSerializer):
    """
    serializers for questions
    """
    user = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Votes
        fields = (
            'user', 'question', 'vote', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_user(self, obj):
        return obj.user.username

    def get_question(self, obj):
        return obj.question.content

    def create(self, validated_data):
        question = validated_data['question']
        current_user = validated_data['user']
        user_vote = validated_data['vote']

        if question.user == current_user:
            raise ValidationError('You cannot vote for your own question')

        # Get question vote by current user
        rating = question.ratings.filter(user=current_user).first()

        # if vote exist just update the vote
        if rating:
            if rating.vote == user_vote:
                user_vote = 0
            rating.vote = user_vote
            rating.save()
        else:
            # if vote not found then create the vote
            question.ratings.create(user=current_user, vote=user_vote)

        # return that rating to be displayed to the user
        return question.ratings.get(user=current_user, vote=user_vote)
