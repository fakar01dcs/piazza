from datetime import datetime, timedelta

from django.db import models


class Topic(models.Model):
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
    topic = models.ManyToManyField(Topic)

    title = models.CharField(max_length=60,primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField()
    name = models.CharField(max_length=60)
    expiration_time = models.DurationField()

    def __str__(self):
        return self.title

class Interaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    comment = models.TextField(default='',blank=True)

    def save(self, *args, **kwargs):
        self.post = Post.objects.exclude(
            name__iexact=self.name).get(
                timestamp__gt=datetime.now()-models.F('expiration_time'), 
                title__exact=self.post
                )
        super(Interaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

