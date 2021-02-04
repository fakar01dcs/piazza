from rest_framework import serializers
from .models import Post, Interaction

class PostSerializer(serializers.HyperlinkedModelSerializer):
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
        fields = ('title','topic','message_body','total_likes', 'total_dislikes', 'total_comments')