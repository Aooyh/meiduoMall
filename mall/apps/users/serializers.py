from rest_framework import serializers
from users.models import User
from django_redis import get_redis_connection
from rest_framework_jwt.views import api_settings
import re


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='确认密码', required=True, write_only=True)
    allow = serializers.CharField(label='是否同意协议', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, write_only=True)
    token = serializers.CharField(label='jwt验证所需的token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'sms_code', 'allow', 'mobile', 'token']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'max_length': 20,
                'min_length': 5,
                'error_messages': {'max_length': '仅允许5~20字符的用户名', 'min_length': '仅允许5~20字符的用户名'}
            },
            'password': {
                'write_only': True,
                'max_length': 20,
                'min_length': 8,
                'error_messages': {'max_length': '仅允许8~20字符的密码', 'min_length': '仅允许8~20字符的密码'}
            },
        }

    def validate_mobile(self, value):
        """
        手机号合法性校验
        """
        if not re.match(r'1[356789]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    def validate(self, attrs):
        # 验证是否同意协议
        if attrs.get('allow') != 'true':
            raise serializers.ValidationError('需要同意协议')

        # 验证两次密码是否一致
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次输入密码不一致')

        # 验证手机验证码是否有效
        redis_conn = get_redis_connection('code')
        redis_sms = redis_conn.get('sms_code_%s' % attrs['mobile']).decode()
        if redis_sms is None:
            raise serializers.ValidationError('验证码已过期')
        if redis_sms != attrs['sms_code']:
            raise serializers.ValidationError('手机验证码输入错误')

        return attrs

    def create(self, validated_data):
        # 删除多余字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # 创建对象
        user = super().create(validated_data)

        # 密码
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        jwt_payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(jwt_payload)
        return user
