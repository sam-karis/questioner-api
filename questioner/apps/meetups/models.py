from django.db import models

# local imports
from questioner.apps.user.models import User

# Create your models here.


class MeetUp(models.Model):
    """
    create a meetup model
    """
    title = models.CharField(max_length=500)
    description = models.TextField(blank=False)
    venue = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500, null=True)
    organizers = models.CharField(max_length=100, blank=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name='admin', on_delete=models.CASCADE)
