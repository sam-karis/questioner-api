from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# local imports
from questioner.apps.helpers.permissions import IsOwnerOrReadOnly
from questioner.apps.meetups.models import MeetUp
from questioner.apps.questions.models import Questions
from questioner.apps.questions.serializers import QusetionSerializer


class CreateGetQuestionsAPIView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QusetionSerializer

    def get_meetup(self):
        meetup_slug = self.kwargs.get('slug')
        meetup = MeetUp.objects.filter(slug=meetup_slug).first()
        if not meetup:
            raise NotFound(f'No meetup related to {meetup_slug} public id.')
        else:
            return meetup

    def post(self, request, **kwargs):
        meetup = self.get_meetup()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(meetup=meetup, user=request.user)

        message = {
            'message': 'question submitted successfully.',
            'data': serializer.data
        }
        return Response(message, status.HTTP_201_CREATED)

    def get(self, request, **kwargs):
        meetup = self.get_meetup()
        queryset = Questions.objects.filter(meetup=meetup, parent=None)
        serializer = self.serializer_class(queryset, many=True)
        message = {'count': queryset.count(), 'questions': serializer.data}
        return Response(message, status.HTTP_201_CREATED)


class SpecificQuestionAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    '''
    Handle getting a profile for specific user
    '''
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = QusetionSerializer

    def get_meetup(self):
        meetup_slug = self.kwargs.get('slug')
        meetup = MeetUp.objects.filter(slug=meetup_slug).first()
        if not meetup:
            raise NotFound(f'No meetup related to {meetup_slug} public id.')
        else:
            return meetup

    def get_object(self):
        meetup = self.get_meetup()
        question_id = self.kwargs.get('id')
        question = Questions.objects.filter(
            meetup=meetup, id=question_id).first()
        if not question:
            raise NotFound(f'No question related to {question_id} id.')
        else:
            self.check_object_permissions(self.request, question)
            return question

    def put(self, request, slug, id):
        '''Edit a question.'''
        question = self.get_object()
        serializer = self.serializer_class(question, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = {
            'message': 'Question updated successfully.',
            'data': serializer.data
        }
        return Response(message, status.HTTP_200_OK)

    def delete(self, request, slug, id):
        '''Delete a question.'''
        super().delete(self, request, slug, id)
        return Response({"message": "Question Deleted Successfully."})

    def post(self, request, slug, id):

        meetup = self.get_meetup()
        question = self.get_object()
        data = {
            'content': request.data.get('content', None),
            'parent': question.pk,
            'meetup': meetup,
            'author': request.user
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(meetup=meetup, user=request.user)

        message = {
            'message': 'question submitted successfully.',
            'data': serializer.data
        }
        return Response(message, status.HTTP_201_CREATED)
