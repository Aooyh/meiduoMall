from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from .models import Area
from .serializers import AreaSerializer, ProvinceSerializer

# Create your views here.


class AreasViewSets(CacheResponseMixin, ReadOnlyModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            self.queryset = Area.objects.filter(parent_id__isnull=True).all()
        else:
            self.queryset = Area.objects.all()
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = ProvinceSerializer
        else:
            self.serializer_class = AreaSerializer
        return self.serializer_class
