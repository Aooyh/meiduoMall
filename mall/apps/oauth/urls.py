from django.conf.urls import url
from . import views

urlpatterns = [
    url('^qq/statues/', views.QQAuthURLView.as_view()),
    url('^qq/users/', views.QQAuthURLView.as_view()),
]