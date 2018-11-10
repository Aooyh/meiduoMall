from django_redis import get_redis_connection
from .models import OAuthQQUser
from users.models import User
from .utils import check_user_token
from rest_framework import serializers


class UserBindSerializer(serializers.Serializer):
    mobile = serializers.RegexField(regex='^1[356789]\d{9}$', label='用户手机号')
    sms_code = serializers.CharField(max_length=6, min_length=6, label='短信验证码')
    access_token = serializers.CharField(label='包含openid的通行证')
    password = serializers.CharField(min_length=8, max_length=20, label='密码')

    def validate(self, attrs):
        redis_conn = get_redis_connection('code')
        user_mobile = attrs['mobile']
        redis_sms = redis_conn.get('sms_code_%s' % user_mobile).decode()
        openid = check_user_token(attrs['access_token']).get('openid')
        if not openid:
            raise serializers.ValidationError('无效的操作凭证')
        if redis_sms != attrs['sms_code']:
            raise serializers.ValidationError('手机验证码错误')
        attrs['openid'] = openid
        try:
            user = User.objects.get(mobile=user_mobile)
        except User.DoesNotExist:
            pass
        else:
            attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        mobile = validated_data['mobile']
        password = validated_data['password']
        username = validated_data['mobile']
        if user:
            if not user.check_password(password):
                raise serializers.ValidationError('密码不正确')
        else:
            user = User.objects.create(username=username, mobile=mobile, password=password)
            user.set_password(password)
        qq_user = OAuthQQUser.objects.create(user=user, openid=validated_data['openid'])
        return qq_user
