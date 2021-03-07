from datetime import datetime

from django.db.models import Sum, Aggregate, CharField, F, Func, Case, Value, When
from django.utils import timezone

# Create your views here.
from rest_framework import viewsets
from .serializers import PostSerializer, InteractionSerializer, TopicSerializer
from .models import Post, Interaction, Topic
 
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
