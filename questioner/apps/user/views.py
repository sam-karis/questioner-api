from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

# local imports
from questioner.apps.user.models import Profile
from questioner.apps.user.serializers import (
    RegisterSerializer, LoginSerializer, GetProfileSerializer,
    )
from questioner.apps.helpers.permissions import IsOwnerOrReadOnly


class RegisterUserAPIView(APIView):
    '''
    Handles user registration
    '''
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = {
            'message': 'User registered successfully.',
            'data': serializer.data
        }
        return Response(message, status.HTTP_201_CREATED)


class LoginUserAPIView(APIView):
    '''
    Handles user login
    '''
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SpecificUserProfileAPIView(RetrieveUpdateDestroyAPIView):
    '''
    Handle getting a profile for specific user
    '''
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = GetProfileSerializer

    def get_object(self):
        try:
            username = self.kwargs.get('username')
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise NotFound(f'No profile related to {username} username')
        else:
            self.check_object_permissions(self.request, profile)
            return profile


class GetAllProfileAPIView(ListAPIView):
    '''
    Handle getting of user profiles
    '''

    permission_classes = (IsAuthenticated,)
    serializer_class = GetProfileSerializer
    queryset = Profile.objects.all()
