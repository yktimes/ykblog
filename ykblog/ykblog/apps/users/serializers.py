from rest_framework import serializers
from .models import User,FriendShip
import re

from rest_framework_jwt.settings import api_settings
from hashlib import md5

def generate_avatar(email, size):
    '''头像'''
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class UserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """
    # token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
    # _linkes = serializers.HyperlinkedIdentityField(read_only=True,view_name='user-retrieve')
    class Meta:
        model = User
        fields = ("username","email","password")

        # read_only_fields = ('_linkes',)

        extra_kwargs = {
            'password': {'write_only': True},

        }

    def create(self, validated_data):
        """
        创建用户
        """

        user = super().create(validated_data)
        user.avatar=generate_avatar(user.email,128)
        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # # 补充生成记录登录状态的token
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # payload = jwt_payload_handler(user)
        # token = jwt_encode_handler(payload)
        # user.token = token

        return user


class MySerializer(serializers.Serializer):
    """数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    username = serializers.CharField(label='注册名称',max_length=30, required=False)
    name = serializers.CharField(label='名称', max_length=30,required=False)
    avatar = serializers.CharField(label='发布日期',max_length=255, required=False)
    followeds_count = serializers.IntegerField(label='关注', required=False)
    followers_count = serializers.IntegerField(label='粉丝', required=False)
    is_following = serializers.BooleanField(label='是否关注', required=False)
    date=serializers.DateTimeField(required=False)

class Mysite(serializers.ModelSerializer):



    class Meta:
        model = User
        fields = ('id','username', 'email','name','location','about_me',"date_joined","avatar",'is_staff')

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户修改信息序列化器
    """
    class Meta:
        model = User
        fields = ('username', 'email')

        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},

        }



    def validate_email(self, value):
        """验证邮箱"""

        # 邮箱是否重复
        try:
            email = User.objects.get(email=value)
            raise serializers.ValidationError('邮箱已存在')
        except User.DoesNotExist as e:

            return value


    def validate_username(self, value):



        # 用户名是否重复
        try:
            user = User.objects.get(username=value)
            raise serializers.ValidationError('用户名已存在')
        except User.DoesNotExist as e:

            return value


class UserUpdatev2Serializer(serializers.ModelSerializer):
    """
    用户修改信息序列化器
    """
    class Meta:
        model = User
        fields = ('name', 'location','about_me')

        extra_kwargs = {
            'name': {'required': False},
            'location': {'required': False},
            'about':{'required': False},
        }

class FollowerSerializers(serializers.ModelSerializer):
    follower = Mysite(read_only=True)
    class Meta:
        model = FriendShip

        fields = ('follower',  'date')


class FollowedSerializers(serializers.ModelSerializer):
    followed = Mysite(read_only=True)
    class Meta:
        model = FriendShip

        fields = ('followed',  'date')
from posts.models import Likedship

from posts.serializers import LikedCommentSerializer,UserPostInfo,PostLikeSerializer

class LiedSerializers(serializers.ModelSerializer):
    user=UserPostInfo()
    comment = LikedCommentSerializer()
    class Meta:
        model = Likedship
        fields = ('comment', 'user','timestamp')


from posts.models import LikedPost
class LikedPostSerializers(serializers.ModelSerializer):
    user=UserPostInfo()
    post = PostLikeSerializer()
    class Meta:
        model = LikedPost
        fields = ('post', 'user','timestamp')

