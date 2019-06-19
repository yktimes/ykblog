from django.shortcuts import render
from posts.models import Post
# Create your views here.
from rest_framework  import status
from rest_framework.views import APIView

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
class s(APIView):
    pass

class PostViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):

    # queryset和serializer_class是固定写法
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    @permission_classes((IsAuthenticated,))
    def post(self, request, *args, **kwargs):
        # return self.create(request, *args, **kwargs)
        print(request.user)

        serializer = self.get_serializer(data=request.data)


        if serializer.is_valid():
            print(serializer.data)
            title=serializer.data.get('title')
            body=serializer.data.get('body')
            summary=serializer.data.get('summary')
            author=request.user

            print("sssssss",summary)
            post = Post.objects.create(title=title,body=body,summary=summary,author=author)


            return Response({'status': 'ok', 'id': post.pk, 'title':post.title,})

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        # return self.create(request, *args, **kwargs)
from rest_framework.permissions import IsAuthenticated

class PostViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)

    @permission_classes((IsAuthenticated,))
    def put(self, request, *args, **kwargs):
        # TODO 设置 permission_classes 开启

        user = request.user
        print(user.pk)
        if int(request.user.pk) == int(self.get_object().author.pk):
            return self.update(request, *args, **kwargs)


    @permission_classes((IsAuthenticated,))
    def delete(self, request, *args, **kwargs):
        # 判断要删除的帖子用户是否和请求用户一致

        instance = self.get_object()
        if int(request.user.pk) == int(instance.author.pk):
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
