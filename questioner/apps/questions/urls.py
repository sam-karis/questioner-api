from django.urls import path

# local imports
from questioner.apps.questions.views import (
    CreateGetQuestionsAPIView, SpecificQuestionAPIView, VoteAPIView
)

app_name = 'questions'

urlpatterns = [
    path('meetups/<slug>/questions/', CreateGetQuestionsAPIView.as_view(),
         name='create_get_questions'),
    path('meetups/<slug>/questions/<id>',
         SpecificQuestionAPIView.as_view(), name='specific_question'),
    path('meetups/<slug>/questions/<id>/vote/',
         VoteAPIView.as_view(), name='specific_question'),
]
