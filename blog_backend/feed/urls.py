from django.urls import path

from . import api
from . import views

urlpatterns = [
    path("create/", api.create_post, name="api_create_post"),
    path("", api.posts_list, name="api_posts_list"),
    path('<str:pk>/', views.PostDetailView.as_view(), name='post-detail'),
]