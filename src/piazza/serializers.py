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
    status = serializers.CharField(
        read_only=True
    )           
    class Meta:
        model = Post
        fields = ('title','topic', 'name','message_body','total_likes', 'total_dislikes',
         'total_comments', 'timestamp', 'expiration_time', 'status')


class InteractionSerializer(serializers.ModelSerializer):
    time_left_till_expiry = serializers.DurationField(
        read_only=True
        )   
    class Meta:
        model = Interaction
        fields = ('post', 'name', 'like', 'dislike', 'comment', 'time_left_till_expiry')

    def validate(self, data):
        """
        Check that you are not interacting with your own post.
        """
        post = Post.objects.get(title__iexact=data['post'])
        if str(post.name).lower() == str(data['name']).lower():
            raise serializers.ValidationError("Cant interact with your own post")
        return data

class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('__all__')

    


    
