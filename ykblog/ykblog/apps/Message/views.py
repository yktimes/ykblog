
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from .models import Message
from .serializers import CreateMessageSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser

class MessageView(ListModelMixin, GenericAPIView):
    '''给其它用户发送私信'''
    # queryset和serializer_class是固定写法
    queryset = Message.objects.all().select_related('sender', 'recipient')
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):

        body = request.data.get('body').strip()
        recipient_id = request.data.get('recipient_id')



        if len(body.strip()) == 0 :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not recipient_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:

            recipient_user = User.objects.get(id=int(recipient_id))
            print(recipient_user, "成功")
        except User.DoexNotExist:
            return Response({'message':'该用户可能在火星上哦'},status=status.HTTP_404_NOT_FOUND)
        else:
            user =request.user

            # 如果你在对方黑名单或者对方在你黑名单
            if recipient_user.is_blocking(user) or user.is_blocking(recipient_user):
                return Response({'message':'被人家或自己屏蔽了'},status=status.HTTP_400_BAD_REQUEST)

            #　自己不能发私信
            if user.pk==recipient_user.pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                Message.objects.create(body=body,recipient=recipient_user,sender=user)
                # 给私信接收者发送新私信通知
                recipient_user.add_notification('unread_messages_count',
                                      recipient_user.new_recived_messages())


            return Response(status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MessagesViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Message.objects.all().select_related('sender', 'recipient')
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated,]
    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):


        instance = self.get_object()


        user = request.user
        # 　自己不能发私信
        if user.pk == instance.recipient_user.pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        instance.recipient.add_notification('unread_messages_count',
                                           instance.recipient.new_recived_messages())
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessagesAllView(APIView):
    permission_classes = [IsAdminUser,]
    def post(self,request):
        '''群发私信'''
        user = request.user


        data = request.data
        if not data:
            return   Response({'message': 'You must post JSON data.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'body' not in data or not data.get('body'):
            return Response({'message': {'body': 'Body is required.'}}, status=status.HTTP_400_BAD_REQUEST)


        #  celery 群发私信
        user.launch_task('send_messages', '正在群发私信...',
                                   kwargs={'user_id': user.pk, 'body': data.get('body')})
        return Response({'message': '正在运行群发私信后台任务'},status=status.HTTP_200_OK)