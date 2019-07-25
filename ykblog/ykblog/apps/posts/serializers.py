from rest_framework import serializers

from .models import Post,Comment
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
        fields = ("id", "title", "body", 'summary', 'author','views','comments_count')

        read_only_fields = ('id', 'author','views')


class PostAuthorSerializer(serializers.ModelSerializer):
    """
    创建博客用户序列化器
    """
    # author = UserPostInfo(read_only=True)

    class Meta:
        model = Post
        fields = ("id",  'author')

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

class CreateWallCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'body', 'parent_id')

        extra_kwargs = {
            'parent_id': {'required': False, },
        }

    # def validate_post(self, attrs):

    def validate_body(self, value):
        """评论内容，不能为空"""
        if not value.strip():
            raise serializers.ValidationError('评论不能为空')

        return value



class CommentSerializer(serializers.ModelSerializer):
    author = UserPostInfo()
    post = PostAuthorSerializer()

    class Meta:
        model = Comment
        fields = ('id','body','timestamp','mark_read','disabled','author','parent','post','liked')



class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title',)

class MyCommentSerializer(serializers.ModelSerializer):
    author = UserPostInfo()
    post = CommentPostSerializer()

    class Meta:
        model = Comment
        fields = ('id','body','timestamp','mark_read','disabled','author','post')


