from django.db import models

# Create your models here.
class Post(models.Model):
    TOPIC_CHOICES = (
        ('POLITICS', 'Politics'),
        ('HEALTH', 'Health'),
        ('SPORT', 'Sport'),
        ('TECH','Tech')
    )
    STATUS_CHOICES = (
        ('LIVE', 'Live'),
        ('EXPIRED', 'Expired')
    )
    title = models.CharField(max_length=60)
    topic = models.CharField(max_length=8, choices=TOPIC_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField()
    expiration = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    name = models.CharField(max_length=60)

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