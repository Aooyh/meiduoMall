from django.http import HttpResponse
from django_redis import get_redis_connection
from celery_tasks.main import app
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from libs.captcha.captcha import captcha
from random import randint
from .serializers import SmsCodeSerializer
import logging

# Create your views here.

logger = logging.getLogger('meiduo')


class RegisterImageCode(APIView):
    """
    accept code uuid
    return code image
    """
    @staticmethod
    def get(request, image_code_id):
        redis_conn = get_redis_connection('code')
        name, text, image = captcha.generate_captcha()
        redis_conn.set('img_%s' % image_code_id, text, 60)
        return HttpResponse(image, content_type='image/jpeg')


class RegisterSmsCode(APIView):
    """
    verify image code and mobile
    send text message
    """
    @staticmethod
    def get(request, mobile):
        redis_conn = get_redis_connection('code')

        # 参数校验
        params = request.query_params
        serializer = SmsCodeSerializer(data=params)
        serializer.is_valid(raise_exception=True)

        # 查看用户是否频繁获取
        if redis_conn.get('sms_flag_%s' % mobile):
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

        sms_code = '%06d' % randint(0, 999999)

        # 在redis中设置短信接用户缓存
        redis_conn.set('sms_code_%s' % mobile, sms_code, 300)
        redis_conn.set('sms_flag_%s' % mobile, 1, 60)

        # 发送短信, 利用celery异步发送
        app.send_task('send_sms_code', (mobile, sms_code))
        return Response({'message': 'ok'})
