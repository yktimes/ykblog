from rest_framework import serializers
from .models import User
import re

from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
    # _linkes = serializers.HyperlinkedIdentityField(read_only=True,view_name='user-retrieve')
    class Meta:
        model = User
        fields = ("username","email","password","token")

        # read_only_fields = ('_linkes',)

        extra_kwargs = {
            'password': {'write_only': True},

        }

    def create(self, validated_data):
        """
        创建用户
        """

        user = super().create(validated_data)

        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user


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


