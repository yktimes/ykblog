from rest_framework import serializers

from .models import Post,Comment
from users.models import User


class UserPostInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', "avatar",'is_staff')


class PostSerializer(serializers.ModelSerializer):
    """
    创建博客序列化器
    """
    author = UserPostInfo(read_only=True)
    likers = UserPostInfo(read_only=True,many=True)
    class Meta:
        model = Post
        fields = ("id", "title", "body", 'summary', 'author','views','comments_count','likers','likers_count','timestamp')

        read_only_fields = ('id', 'author','views','likers','likers_count','timestamp')


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
        fields = ('id','body','timestamp','mark_read','disabled','author','post','liked', 'parent_id')



class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title')

class MyCommentSerializer(serializers.ModelSerializer):
    author = UserPostInfo()
    post = CommentPostSerializer()

    class Meta:
        model = Comment
        fields = ('id','body','timestamp','mark_read','disabled','author','post','parent_id')


class LikedCommentSerializer(serializers.ModelSerializer):
    post = CommentPostSerializer()

    class Meta:
        model = Comment
        fields = ('id','body','timestamp','mark_read','disabled','post','liked','parent_id')



class PostLikeSerializer(serializers.ModelSerializer):
    """
    喜欢文章
    """
    class Meta:
        model = Post
        fields = ("id", "title",'likers','likers_count')

        read_only_fields = ('id','likers')