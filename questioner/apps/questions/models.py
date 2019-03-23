from django.db import models

# local imports
from questioner.apps.user.models import User
from questioner.apps.meetups.models import MeetUp


class Questions(models.Model):
    """
    create a meetup model
    """
    content = models.TextField(max_length=1000, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name='questions', on_delete=models.CASCADE)
    meetup = models.ForeignKey(
        MeetUp, related_name='questions', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='threads',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Votes(models.Model):
    """
    create a question vote model
    """
    rate_choices = (
        (-1, 'down_vote'),
        (0, 'no_vote'),
        (1, 'up_vote')
    )
    vote = models.SmallIntegerField(choices=rate_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name='ratings', on_delete=models.CASCADE)
    question = models.ForeignKey(
        Questions, related_name='ratings', on_delete=models.CASCADE)

    def __str__(self):
        return self.rate
