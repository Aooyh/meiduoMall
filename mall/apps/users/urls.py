from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/', views.RegisterGetUserName.as_view(), name='username_count'),
    url(r'^phones/(?P<mobile>1[35789]\d{9})/count/', views.RegisterGetMobile.as_view(), name='mobile_count'),
]
