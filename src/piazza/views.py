from datetime import timedelta, datetime

from django.db.models import Sum, Aggregate, CharField
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from .serializers import PostSerializer, InteractionSerializer, TopicSerializer
from .models import Post, Interaction, Topic
from rest_framework.response import Response

from django.db.models import Aggregate, CharField, F, Func
 
class Concat(Aggregate):
    """ORM is used to group other fields. This is equivalent to group_concat"""
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'
 
    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)


class PostsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Post.objects.annotate(
            total_likes = Sum('interaction__like'),
            total_dislikes = Sum('interaction__dislike'),
            total_comments = Concat('interaction__comment')
            #status = Func(F('post__timestamp'), F('post__expiration_time_minutes'), function='status')
        )
    """
    def status(timestamp, expiration_time):
        if timestamp + timedelta(minutes=expiration_time):
            return 'Live'
        else:
            return 'Expired'
    """
    queryset = Post.objects.all().order_by('name')
    serializer_class = PostSerializer

class InteractionsViewSet(viewsets.ModelViewSet):

    queryset = Interaction.objects.all().order_by('name')
    serializer_class = InteractionSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('topic')
    serializer_class = TopicSerializer
