from .models import Area
from rest_framework import serializers


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['id', 'name']


class AreaSerializer(serializers.ModelSerializer):
    subs = ProvinceSerializer(many=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
