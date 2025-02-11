from rest_framework import serializers
from .models import CustomUser, Point, Review, Term

"""POINT SERIALIZER"""
class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'

"""USER SERIALIZER"""
class CustomUserSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

"""REVIEW SERIALIZER"""
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

"""TERM SERIALIZER"""
class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'