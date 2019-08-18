from rest_framework import serializers

from users.models import User
from .models import  Message

class UserMessageInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', "avatar")


class CreateMessageSerializer(serializers.ModelSerializer):
    """
    创建私信序列化器
    """
    sender = UserMessageInfo()
    recipient = UserMessageInfo()
    # 设置日期格式化格式
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Message
        fields = ("id", "body", "timestamp", 'sender', 'recipient')


