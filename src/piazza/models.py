from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    TOPIC_CHOICES = (
        ('POLITICS', 'Politics'),
        ('HEALTH', 'Health'),
        ('SPORT', 'Sport'),
        ('TECH','Tech')
    )
    title = models.CharField(max_length=60)
    topic = models.CharField(max_length=8, choices=TOPIC_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField()
    name = models.CharField(max_length=60)

    def expiration(self):
        return self.timestamp + timedelta(days=1)

    def status(self):
        return 'LIVE' if timezone.now() < (self.timestamp + timedelta(days=1)) else 'EXPIRED'

    def __str__(self):
        return self.title

class Interaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, limit_choices_to={'status': 'LIVE'})
    name = models.CharField(max_length=60)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    comment = models.TextField(default='')
    time_left = models.DateTimeField()

    def __str__(self):
        return self.name