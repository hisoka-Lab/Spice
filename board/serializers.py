from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'body', 'created_at']
        read_only_fields = ['author', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model, including nested comments."""
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'author_name', 'created_at', 'comments']
        read_only_fields = ['author', 'created_at']
