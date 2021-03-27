from datetime import datetime

from django.db.models import Sum, Aggregate, CharField, F, Func, Case, Value, When
from django.utils import timezone

# Create your views here.
from rest_framework import viewsets
from .serializers import PostSerializer, InteractionSerializer, TopicSerializer
from .models import Post, Interaction, Topic
 

class Concat(Aggregate):
    """Group concat function to concat strings of comments into a list, found at
     https://stackoverflow.com/questions/10340684/group-concat-equivalent-in-django/40478702#40478702"""
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'
 
    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)


class PostsViewSet(viewsets.ModelViewSet):
    """Define the viewset for posts, with additional annotations for total likes, 
    dislikes, comments and status"""
    def get_queryset(self):
        return Post.objects.annotate(
            total_likes = Sum('interaction__like'),
            total_dislikes = Sum('interaction__dislike'),
            total_comments = Concat('interaction__comment'),
            status = Case(
                When(timestamp__lt=timezone.make_aware(datetime.now()) - F('expiration_time'), then=Value('Expired')),
                default=Value('Live'),
                output_field=CharField()
        ))  
    queryset = Post.objects.all().order_by('name')
    serializer_class = PostSerializer

class InteractionsViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all().order_by('name')
    serializer_class = InteractionSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('topic')
    serializer_class = TopicSerializer
