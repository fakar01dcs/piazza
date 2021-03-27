from rest_framework import serializers
from django.contrib.auth.models import User

class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer class used in lab4 cloud computing"""
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
        'password': {'write_only': True}
        }