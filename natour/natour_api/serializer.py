from rest_framework import serializers
from .models import CustomUser, Point

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
    