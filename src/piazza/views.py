from django.db.models import Sum, Aggregate, CharField
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post, Interaction

from django.db.models import Aggregate, CharField
 
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
        )
    queryset = Post.objects.all().order_by('name')
    serializer_class = PostSerializer