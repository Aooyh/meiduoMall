from itsdangerous import TimedJSONWebSignatureSerializer as JWSSerializer, BadData
from mall import settings


def generate_save_user_token(openid):
    serializer = JWSSerializer(settings.SECRET_KEY, 3600)
    data = {'openid': openid}
    token = serializer.dumps(data)
    return token.decode()


def check_user_token(token):
    serializer = JWSSerializer(settings.SECRET_KEY, 3600)
    try:
        data = serializer.loads(token)
    except BadData:
        data = None
    return data
