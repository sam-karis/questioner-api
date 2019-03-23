from rest_framework.views import APIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from django.db.models import Sum, Count
# local imports
from questioner.apps.helpers.permissions import IsOwnerOrReadOnly
from questioner.apps.meetups.models import MeetUp
from questioner.apps.questions.models import Questions
from questioner.apps.questions.serializers import (
    QusetionSerializer, VotesSerializer
)


class QuestionBaseAPIView(APIView):
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


class CreateGetQuestionsAPIView(QuestionBaseAPIView, APIView):
    '''
    Handle creating and getting all questions for specific meetup
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QusetionSerializer

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


class SpecificQuestionAPIView(QuestionBaseAPIView, RetrieveDestroyAPIView):
    '''
    Handle specific question for specific meetup
    '''
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = QusetionSerializer

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


class VoteAPIView(QuestionBaseAPIView):
    '''
    Handle up and down voting specific questions
    '''
    permission_classes = (IsAuthenticated, )
    serializer_class = VotesSerializer

    def post(self, request, slug, id):
        question = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question=question, user=request.user)

        message = {
            'message': 'Vote submitted successfully.',
            'data': serializer.data
        }
        return Response(message, status.HTTP_201_CREATED)

    def get(self, request, slug, id):
        question = self.get_object()
        ratings = question.ratings.all()
        serializer = self.serializer_class(ratings, many=True)

        # get sum of all votes and number of user who have voted
        votes_sum_count = ratings.aggregate(
            vote_sum=Sum('vote'), vote_count=Count('vote'))
        # get question votes frequency
        vote_names = {-1: 'down_vote', 0: 'no_vote', 1: 'up_vote'}
        vote_freq = ratings.values_list('vote').annotate(Count('vote'))
        vote_freq = {vote_names[key]: value for (key, value) in vote_freq}

        message = {
            'summary': {**votes_sum_count, **vote_freq},
            'data': serializer.data
        }
        return Response(message, status.HTTP_201_CREATED)
