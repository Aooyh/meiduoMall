from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from celery_tasks.email.tasks import send_verify_mail
from itsdangerous import TimedJSONWebSignatureSerializer as JWSSerializer, BadSignature
from mall import settings
from .serializers import RegisterSerializer, EmailUpdateSerializer
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


class UserInfoAPIView(APIView):
    """
    用户个人中心
    """
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        username = user.username
        mobile = user.mobile
        email = user.email
        email_active = user.email_active
        data = {
            'username': username,
            'mobile': mobile,
            'email': email,
            'email_active': email_active
        }
        return Response(data=data)


def make_jws_serializer():
    jws_serializer = JWSSerializer(settings.SECRET_KEY, 3600)
    return jws_serializer


class SendEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        user = request.user
        data = request.data

        # 验证数据更新用户邮箱
        serializer = EmailUpdateSerializer(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 发送验证邮件到用户设置的邮箱
        recv_email = data.get('email')
        data = {'user_id': user.id}
        jws_serializer = make_jws_serializer()
        verify_token = jws_serializer.dumps(data)
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + verify_token.decode()

        # 异步celery任务发送邮件
        send_verify_mail.delay(recv_email, verify_url)

        return Response({'messages': '邮箱已更改,确认邮件已发送'})


class EmailVerifyAPIView(APIView):
    @staticmethod
    def get(request):
        # 验证token合法性, 获取用户
        verify_token = request.query_params.get('token')
        jws_serializer = make_jws_serializer()
        try:
            user_id = jws_serializer.loads(verify_token).get('user_id')
        except BadSignature:
            raise BadSignature

        # 激活该用户设置的邮箱
        user = User.objects.filter(id=user_id)
        user.update(email_active=True)
        return Response({'message': '邮箱验证成功'})
