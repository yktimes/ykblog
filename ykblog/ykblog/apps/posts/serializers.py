from rest_framework import serializers

from .models import Post
from users.models import User


class UserPostInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', "avatar")


class PostSerializer(serializers.ModelSerializer):
    """
    创建博客序列化器
    """
    author = UserPostInfo(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "body", 'summary', 'author')

        read_only_fields = ('id', 'author')


class PostListSerializer(serializers.ModelSerializer):
    """

    """
    author = UserPostInfo()

    # token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
    # _linkes = serializers.HyperlinkedIdentityField(read_only=True,view_name='user-retrieve')
    class Meta:
        model = Post
        fields = ("id", "title", "body", 'summary', 'author')

        read_only_fields = ('id',)
