from rest_framework import serializers

from .models import Post, Comment, Category
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class UserPostInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', "avatar", 'is_staff')


class PostTimeSerializer(serializers.ModelSerializer):
    """
    时间轴博客序列化器
    """
    author = UserPostInfo(read_only=True)
    timestamp = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = Post
        fields = ("id", "title", 'timestamp', 'author',)


class PostSerializer(serializers.ModelSerializer):
    """
    创建博客序列化器
    """
    author = UserPostInfo(read_only=True)
    likers = UserPostInfo(read_only=True, many=True)

    # category = CategorySerializer()

    class Meta:
        model = Post
        fields = ("id", "title", "body", 'timestamp', 'summary', 'image', 'author', 'views', 'comments_count', 'likers',
                  'likers_count', 'category')

        read_only_fields = ('id', 'author', 'views', 'likers', 'likers_count', 'timestamp')


class PostAuthorSerializer(serializers.ModelSerializer):
    """
    创建博客用户序列化器
    """

    # author = UserPostInfo(read_only=True)

    class Meta:
        model = Post
        fields = ("id", 'author')

        read_only_fields = ('id', 'author')


class PostListSerializer(serializers.ModelSerializer):
    """

    """
    author = UserPostInfo(read_only=True)
    likers = UserPostInfo(read_only=True, many=True)

    category = CategorySerializer(read_only=True, )

    class Meta:
        model = Post
        fields = (
        "id", "title", "body", 'author', 'timestamp', 'summary', 'likers', 'category', 'views', 'comments_count',
        'likers_count', 'views', 'comments_count', 'likers_count')

        read_only_fields = ('id', 'author', 'views', 'likers', 'likers_count', 'timestamp')


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
    # 设置日期格式化格式
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'timestamp', 'mark_read', 'disabled', 'author', 'post', 'liked', 'parent_id')


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title')


class MyCommentSerializer(serializers.ModelSerializer):
    author = UserPostInfo()
    post = CommentPostSerializer()
    # 设置日期格式化格式
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'timestamp', 'mark_read', 'disabled', 'author', 'post', 'parent_id')


class LikedCommentSerializer(serializers.ModelSerializer):
    post = CommentPostSerializer()
    # 设置日期格式化格式
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'timestamp', 'mark_read', 'disabled', 'post', 'liked', 'parent_id')


class PostLikeSerializer(serializers.ModelSerializer):
    """
    喜欢文章
    """

    class Meta:
        model = Post
        fields = ("id", "title", 'likers', 'likers_count')

        read_only_fields = ('id', 'likers')


from drf_haystack.serializers import HaystackSerializer
from .search_indexes import PostIndex


class PostSearchSerializer(serializers.ModelSerializer):
    """
    文章序列化器
    """

    class Meta:
        model = Post
        fields = ('id', 'title', 'summary', 'body')


class PostIndexSerializer(HaystackSerializer):
    """
    文章索引结果数据序列化器
    """
    object = PostListSerializer(read_only=True)

    class Meta:
        index_classes = [PostIndex]
        fields = ('text', object)


class PostLikeMoreSerializer(serializers.ModelSerializer):
    """
    围观最多的文章
    """

    class Meta:
        model = Post
        fields = ("id", "title", "views")
