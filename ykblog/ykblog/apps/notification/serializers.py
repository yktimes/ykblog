
from rest_framework import serializers

from .models import Notification

from users.models import User


class UserNotificationInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', "avatar")

class NotificationSerializer(serializers.ModelSerializer):
    """动态序列化器"""
    author = UserNotificationInfo(read_only=True)


    class Meta:
        model = Notification

        fields = ('id', 'name','payload_json','timestamp',"author")