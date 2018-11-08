from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views


urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/', views.RegisterGetUserName.as_view(), name='username_count'),
    url(r'^phones/(?P<mobile>1[35789]\d{9})/count/', views.RegisterGetMobile.as_view(), name='mobile_count'),
    url(r'^$', views.RegisterCreateView.as_view(), name='user_register'),
    url(r'^auths/', obtain_jwt_token, name='auth')
]
