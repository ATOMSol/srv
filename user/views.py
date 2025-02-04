from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers.LoginSerializer import LoginSerializer
from user.serializers.UserSerializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework import viewsets

class LoginAPI(viewsets.ViewSet):
    def create(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if serializer.is_valid():
                username = data['username']
                password = data['password']
                user = authenticate(username=username, password=password)

                if user is None:
                    return self.error_response('invalid_password', 'Invalid password')

                if Token.objects.filter(user=user).exists():
                    Token.objects.get(user=user).delete()
                token = Token.objects.create(user=user)

                return Response({
                    'user': UserSerializer(user, many=False).data,
                    'Token': token.key,
                })

            else:
                return self.error_response('invalid_data', 'Invalid data', serializer.errors)

        except Exception as e:
            return self.error_response('something_went_wrong', 'Something went wrong')

    def error_response(self, error, message, data={}):
        return Response({
            'status': 400,
            'error': error,
            'message': message,
            'data': data
        }, status=400)
    

from rest_framework import status


class LogoutView(viewsets.ViewSet):
    def create(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            Token.objects.get(key=token).delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to log out'}, status=status.HTTP_400_BAD_REQUEST)
        


def index(request):
    # Return a HTTP response
    return HttpResponse("Hello, world! You're at the index page.")