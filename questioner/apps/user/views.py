from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# local imports
from questioner.apps.user.serializers import (
    RegisterSerializer, LoginSerializer
)


class RegisterUserAPIView(APIView):
    '''
    Handles user registration
    '''
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # import pdb; pdb.set_trace()
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
