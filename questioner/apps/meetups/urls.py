from django.urls import path
from django.conf.urls import url

from questioner.apps.meetups.views import (
    CreateMeetUpAPIView, SpecificMeetUpAPIView, OwnerMeetUpAPIView
)

app_name = 'meetups'

urlpatterns = [
    path('meetups/', CreateMeetUpAPIView.as_view(), name='create_meetup'),
    path(
        'meetups/user/', OwnerMeetUpAPIView.as_view(),
        name='specific_user_meetups'),
    url(
        r'^meetups/(?P<meetup_id>(\d+))$',
        SpecificMeetUpAPIView.as_view(), name='meetup_by_id'
    ),
]
