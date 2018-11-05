from django.http import HttpResponse
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from rest_framework import status
from rest_framework.response import Response
from django_redis import get_redis_connection
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
