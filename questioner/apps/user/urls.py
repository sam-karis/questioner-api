from django.urls import path
from django.conf.urls import url

from questioner.apps.user.views import (
    RegisterUserAPIView, LoginUserAPIView, SpecificUserProfileAPIView,
    GetAllProfileAPIView
)

app_name = 'auth'

urlpatterns = [
    path('users/', RegisterUserAPIView.as_view(), name='register_user'),
    path('users/login/', LoginUserAPIView.as_view(), name='login_user'),
    path('users/profiles/', GetAllProfileAPIView.as_view(), name='profiles'),
    url(
        r'^users/profiles/(?P<username>[a-zA-Z0-9]+)$',
        SpecificUserProfileAPIView.as_view(), name='user_profile'
        ),
]
