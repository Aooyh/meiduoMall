from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import AreasViewSets

areas_router = DefaultRouter()
areas_router.register(r'^infos', AreasViewSets, base_name='area')

urlpatterns = [
    url(r'^', include(areas_router.urls))
]
