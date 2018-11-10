from rest_framework.views import Response, status
from rest_framework_jwt.settings import api_settings
from .serializers import UserBindSerializer
from .utils import generate_save_user_token
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from oauth.models import OAuthQQUser
from mall import settings
import logging


logger = logging.getLogger('meiduo')

# Create your views here.


class QQAuthURLView(APIView):
    """
    qq 登录
    """
    @staticmethod
    def generate_jwt_user(qq_user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        user = qq_user.user
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

    def get(self, request):
        # 创建验证对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state='/')

        # 提供QQ登录页面网址
        if 'state' in request.query_params:
            # state表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
            state = request.query_params.get('state')
            if state:
                oauth.state = state
            # 获取QQ登录页面网址
            login_url = oauth.get_qq_url()
            return Response({'login_url': login_url})

        # QQ 登录后重定向到指定的页面并带有 code
        # 前端再次发送请求带上参数 code
        # 通过code获取 access_token 并通过 access_token 获取 openid
        if 'code' in request.query_params:
            code = request.query_params.get('code')
            if not code:
                return Response({'message:' '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                access_token = oauth.get_access_token(code)
                openid = oauth.get_open_id(access_token)
            except Exception as e:
                logger.error(e)
                return Response({'message': '服务器异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 通过 openid 验证该用户是否已经绑定
            # 若未绑定, 返回access_token
            # 若已绑定, 返回被 jwt 加密用户的user_id, username 和 token值
            try:
                qq_user = OAuthQQUser.objects.get(openid=openid)
            except OAuthQQUser.DoesNotExist:
                access_token_openid = generate_save_user_token(openid)
                return Response({'access_token': access_token_openid})
            else:
                return self.generate_jwt_user(qq_user)

    def post(self, request):
        # 接收前端传送的数据进行校验
        # 校验完成将绑定完成的 user 信息讲过 jwt 加密返回
        serializer = UserBindSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qq_user = serializer.save()
        return self.generate_jwt_user(qq_user)
