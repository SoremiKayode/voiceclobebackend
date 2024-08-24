from rest_framework import serializers
from .models import User, Audio

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    full_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField()
    is_admin = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.save()
        return instance

class AudioSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    location = serializers.CharField(required=False)  # File path may not be present
    text = serializers.CharField()
    user = serializers.CharField()  # This will hold the user ID
    datetime = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        audio = Audio(**validated_data)
        audio.save()
        return audio

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.text = validated_data.get('text', instance.text)
        instance.user = validated_data.get('user', instance.user)
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.save()
        return instance