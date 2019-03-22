from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

# Local imports
from questioner.apps.meetups.models import MeetUp
from questioner.apps.meetups.serializers import MeetUpSerializer
from questioner.apps.helpers.permissions import (
    IsAdminUserOrReadonly, IsOwnerOrReadOnly)
from questioner.apps.helpers.utils import ConvertDate


class CreateMeetUpAPIView(ListCreateAPIView):

    permission_classes = (IsAdminUserOrReadonly,)
    queryset = MeetUp.objects.all()
    serializer_class = MeetUpSerializer

    def post(self, request):
        request.data['start_time'] = ConvertDate.convert_date(
            self, request.data.get('start_time', None))
        request.data['end_time'] = ConvertDate.convert_date(
            self, request.data.get('end_time', None))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        message = {
            'message': 'Meetup created successfully.',
            'data': serializer.data
        }
        return Response(message, status.HTTP_201_CREATED)


class SpecificMeetUpAPIView(RetrieveUpdateDestroyAPIView):
    '''
    Handle getting a profile for specific user
    '''
    queryset = MeetUp.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = MeetUpSerializer

    def get_object(self):
        meetup_slug = self.kwargs.get('slug')
        meetup = MeetUp.objects.filter(slug=meetup_slug).first()
        if not meetup:
            raise NotFound(f'No meetup related to {meetup_slug} public id.')
        else:
            self.check_object_permissions(self.request, meetup)
            return meetup

    def put(self, request, slug):
        meetup = self.get_object()
        if 'start_time' in request.data:
            request.data['start_time'] = ConvertDate.convert_date(
                self, request.data.get('start_time'))
        if 'end_time' in request.data:
            request.data['end_time'] = ConvertDate.convert_date(
                self, request.data.get('end_time'))

        serializer = self.serializer_class(
            meetup, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = {
            'message': 'Meetup updated successfully.',
            'data': serializer.data
        }
        return Response(message, status.HTTP_200_OK)

    def delete(self, request, slug):
        super().delete(self, request, slug)
        return Response({"message": "Meetup Deleted Successfully."})


class OwnerMeetUpAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    queryset = MeetUp.objects.all()
    serializer_class = MeetUpSerializer

    def get(self, request):
        meetups = self.queryset.filter(user=request.user)
        if meetups:
            serializer = MeetUpSerializer(meetups, many=True)
            return Response(serializer.data)
        else:
            message = {'message': "You don't have any meetups yet"}
            return Response(message, status.HTTP_404_NOT_FOUND)
