from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User

# Create your views here.


class RegisterGetUserName(APIView):
    """
    1. accept the username
    2. determine it if exists
    3. return response
    """
    @staticmethod
    def get(request, username):
        count = User.objects.filter(username=username).count()
        return Response(data={'count': count}, status=status.HTTP_200_OK)


class RegisterGetMobile(APIView):
    """
    accept mobile and check it
    """
    @staticmethod
    def get(request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return Response(data={'count': count}, status=status.HTTP_200_OK)


class RegisterCreateView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request)
