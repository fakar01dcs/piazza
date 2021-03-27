from django.urls import include, path
from rest_framework import routers
from . import views

"""Defining end points of the piazza API"""

router = routers.DefaultRouter()
router.register(r'posts', views.PostsViewSet)
router.register(r'interactions', views.InteractionsViewSet)
router.register(r'posttopics', views.TopicViewSet)
urlpatterns = [
 path('', include(router.urls)),
]