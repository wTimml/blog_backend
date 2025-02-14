from rest_framework.generics import RetrieveAPIView
from .models import Post  # Make sure to import your Post model
from .serializers import PostsListSerializer
from rest_framework.permissions import AllowAny


class PostDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]  # Allow any user to access
    queryset = Post.objects.all()
    serializer_class = PostsListSerializer