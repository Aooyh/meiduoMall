from django.conf.urls import url
from . import views

urlpatterns = [
    url('^imagecodes/(?P<image_code_id>.*)/',
        views.RegisterImageCode.as_view(),
        name='image_code_verification'),
    url('^smscodes/(?P<mobile>1[345789]\d{9})/',
        views.RegisterSmsCode.as_view(),
        name='sms_code_verifications'),
]
