from django.db import models
from django.utils.text import slugify
import random

# local imports
from questioner.apps.user.models import User


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
        User, related_name='meetup', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.title

    def generate_slug(self):
        slug = slugify(self.title)
        public_id = self.randomString()
        new_slug = f'{slug}-{public_id}'
        while MeetUp.objects.filter(slug=new_slug).exists():
            public_id = self.randomString()
            new_slug = '{}-{}'.format(slug, public_id)
        return new_slug

    def randomString(self):
        """Generate a random string of fixed length """
        letters = self.title.replace(' ', '').lower()
        return ''.join(random.choice(letters) for i in range(8))

    def save(self, *args, **kwargs):
        """
        Create slug before saving a meetup
        """
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)
