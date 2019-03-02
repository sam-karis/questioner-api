from django.urls import path

from questioner.apps.user.views import (
    RegisterUserAPIView, LoginUserAPIView
)

app_name = 'auth'

urlpatterns = [
    path('users/', RegisterUserAPIView.as_view(), name='register_user'),
    path('users/login/', LoginUserAPIView.as_view(), name='login_user')
]
