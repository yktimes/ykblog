from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from .models import Message
from .serializers import CreateMessageSerializer
from users.models import User
# Create your views here.
class MessageView(ListModelMixin, GenericAPIView):
    '''给其它用户发送私信'''
    # queryset和serializer_class是固定写法
    queryset = Message.objects.all().select_related('sender', 'recipient')
    serializer_class = CreateMessageSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)

        body = request.data.get('body').strip()
        recipient_id = request.data.get('recipient_id')

        print(body, recipient_id)

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

                print(111111111111111111111111111111)
            return Response(status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MessagesViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Message.objects.all().select_related('sender', 'recipient')
    serializer_class = CreateMessageSerializer

    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)

    # @permission_classes((IsAuthenticated,))
    # def put(self, request, *args, **kwargs):
    #     # TODO 设置 permission_classes 开启
    #     instance = self.get_object()
    #
    #
    #     flag = request.data.get('disabled')
    #     mark_read=request.data.get('mark_read')
    #     print("flag",flag,type(flag))
    #     print("mark_read",mark_read,type(mark_read))
    #     # 如果请求用户是该评论用户或着它是该博客主人
    #     # if int(request.user.pk) == int(instance.author.pk) or int(request.user.pk) == int(instance.post.author.pk):
    #
    #     try:
    #         c = Comment.objects.get(pk=self.kwargs['pk'])
    #     except Comment.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         if mark_read is not None:
    #             c.mark_read=True
    #             c.save()
    #         if flag is not None:
    #             c.disabled = flag
    #             c.save()
    #         return Response(status=status.HTTP_200_OK)

    # @permission_classes((IsAuthenticated,))
    def delete(self, request, *args, **kwargs):


        instance = self.get_object()

        # if int(request.user.pk) == int(instance.author.pk) or int(request.user.pk) == int(instance.post.author.pk):

        user = request.user
        # 　自己不能发私信
        if user.pk == instance.recipient_user.pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        # todo给私信接收者发送新私信通知(需要自动减1)
        instance.recipient.add_notification('unread_messages_count',
                                           instance.recipient.new_recived_messages())
        return Response(status=status.HTTP_204_NO_CONTENT)
