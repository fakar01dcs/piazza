from datetime import datetime
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Topic(models.Model):
    """Class representing db of topics"""
    TOPIC_CHOICES = (
        ('Politics', 'Politics'),
        ('Health', 'Health'),
        ('Sport', 'Sport'),
        ('Tech', 'Tech')
    )
    topic = models.CharField(max_length=8, choices=TOPIC_CHOICES, unique=True, primary_key=True)

    def __str__(self):
        return self.topic


class Post(models.Model):
    """Class representing db of posts"""
    topic = models.ManyToManyField(Topic)
    title = models.CharField(max_length=60,primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField()
    name = models.CharField(max_length=60)
    expiration_time = models.DurationField()

    def __str__(self):
        return self.title

class Interaction(models.Model):
    """Class respresenting db of interactions associated to posts"""

    def validate_active(value):
        """Check that the post you are interacting with is live"""
        data = Post.objects.get(title=value)
        if timezone.make_aware(datetime.now()) > (data.timestamp + data.expiration_time):
            raise ValidationError('Post has expired')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, validators=[validate_active])
    name = models.CharField(max_length=60)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    comment = models.TextField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def time_left_till_expiry(self):
        data = Post.objects.get(title=self.post)
        return self.timestamp - data.timestamp

    def __str__(self):
        return self.name

