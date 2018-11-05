from rest_framework import serializers
from django_redis import get_redis_connection
from redis.exceptions import RedisError
import logging

logger = logging.getLogger('meiduo')


class SmsCodeSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=4, min_length=4, required=True, label='user put image_code')
    image_code_id = serializers.CharField(label='image_code uuid')

    def validate(self, attrs):
        image_code = attrs.get('text')
        image_uuid = attrs.get('image_code_id')
        redis_conn = get_redis_connection('code')
        code_text = redis_conn.get('img_%s' % image_uuid)
        if not code_text:
            raise serializers.ValidationError('验证码已过期')
        if code_text.decode().lower() != image_code.lower():
            raise serializers.ValidationError('验证码输入错误')
        try:
            redis_conn.delete(image_uuid)
        except RedisError as e:
            logger.error(e)
        return attrs
