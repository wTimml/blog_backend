from rest_framework import serializers

from .models import Post

# from useraccount.serializers import UserDetailSerializer


class PostsListSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.name')
    author_avatar = serializers.ImageField(source='author.avatar')

        

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'date',
            'author',
            'author_name',
            'author_avatar',
        )

    def get_author_avatar(self, obj):
        return obj.author.avatar_url()