from datetime import datetime, timedelta
from django.utils import timezone


from rest_framework import serializers
from .models import Post, Interaction, Topic


class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(
        read_only=True
        )
    total_dislikes = serializers.IntegerField(
        read_only=True
        )
    total_comments = serializers.CharField(
        read_only=True
    )          
    class Meta:
        model = Post
        fields = ('title','topic', 'name','message_body','total_likes', 'total_dislikes',
         'total_comments', 'timestamp', 'expiration_time')


class InteractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interaction
        fields = ('post', 'name', 'like', 'dislike', 'comment')

class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('__all__')

    


    
