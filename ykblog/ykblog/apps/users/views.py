

from .serializers import *

from . models import User,FriendShip

from rest_framework  import status
from rest_framework.views import APIView

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.generics import GenericAPIView,ListAPIView

from rest_framework.response import Response



class UserViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):

    # queryset和serializer_class是固定写法
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():


            user = serializer.save()

            # '_links': {
            #     'self': reverse("user-retrieve", id=self.id)
            # }
            #
            return Response({'status': 'ok', 'id': user.pk, 'username': user.username})

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # return self.create(request, *args, **kwargs)
from rest_framework.permissions import IsAuthenticated

class UserViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        # is_following={}
        self.serializer_class=Mysite
        user=request.user

        is_following= FriendShip.is_following(user,self.kwargs['pk'])

        data = self.retrieve(request, *args, **kwargs)

        return Response({'data':data.data,'is_following':is_following})
        # try:
        #     user = User.objects.get(id=self.argspk)
        # except User.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        #     # serializer = UserSerializer(user)
        # return Response({'id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # TODO 设置 permission_classes 开启


        print("1111",self.kwargs["pk"])
        print(request.data)
        # users/(?P<pk>\d+)/  self.kwargs["pk"] 得到URLpk
        user = request.user
        print(user.pk)
        if int(request.user.pk) ==int(self.kwargs["pk"]):


            # 获取到原来的信息
            # name = user.name
            # location = user.location

            serializer = UserUpdatev2Serializer(data=request.data)
            if serializer.is_valid():

                user.name=serializer.data['name']
                user.location=serializer.data['location']
                user.about_me=serializer.data['about_me']
                user.save()

                return Response({'status': 'ok', 'id': user.pk, 'username': user.username})

            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        # TODO 危险 需要判断
        print(request)
        if int(request.user.pk) == int(self.kwargs["pk"]):
            return self.destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class UnFollowView(APIView):
    """
    取消关注
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        print("取消关注的")
        print(pk)

        to_user = int(self.kwargs["pk"])

        user = request.user

        print(11111111111,user, to_user)

        try:

            to_use = User.objects.get(pk=to_user)
            FriendShip.unfollow(user, to_use)


        except:
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'ok','status':'success'}, status=status.HTTP_200_OK)


class FollowView(APIView):
    """
    关注
    """
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        print("关注")

        to_user=int(self.kwargs["pk"])

        user = request.user


        try:
            to_user = User.objects.get(pk=to_user)
            FriendShip.follow(user, to_user)


        except:
            return Response({'message': 'error','status':'error'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class FollowerView(ListAPIView):
    """
    粉丝
    关注我的人
    """

    # followeds 是该用户关注了哪些用户列表
    # followers 是该用户的粉丝列表

    def get_queryset(self):


        pk = self.kwargs['pk']
        followers = FriendShip.user_follower(pk)
        if len(followers)>0:
            id = [i.pk for i in followers]
            data = User.objects.filter(id__in=id).values("id", "username", "name", "email", "avatar")
            print(FollowerView)
            print(data)
            # 为每个 follower 添加 其他属性
            for item in data:


                item['is_following'] = FriendShip.is_following(pk,item['id'],)
                # 注意细节
                item['date'] = FriendShip.objects.get(followed=pk, follower=item['id']).date
                item['followeds_count'] = len(FriendShip.user_followed(item['id']))
                item['followers_count'] = len(FriendShip.user_follower(item['id']))

            return data
        else:
            return followers

    def get_serializer(self, *args, **kwargs):
        return MySerializer(self.get_queryset(), many=True)

import datetime


class FollowedView(ListAPIView):

    """
    大神
    该用户关注了哪些用户列表
    """

    # followeds 是该用户关注了哪些用户列表
    # followers 是该用户的粉丝列表


    def get_queryset(self):
        pk = self.kwargs['pk']
        followeds = FriendShip.user_followed(pk)

        if len(followeds)>0:
            id = [i.pk for  i in followeds]
            data = User.objects.filter(id__in=id).values("id","username","name","email","avatar")

            print("FollowedView")
            # 为每个 follower 添加 其他属性
            for item in data:


                item['is_following'] = FriendShip.is_following(pk,item['id'])
                # 注意细节
                item['date'] =FriendShip.objects.get(followed=item['id'], follower=pk).date
                item['followeds_count']=len(FriendShip.user_followed(item['id']))
                item['followers_count'] = len(FriendShip.user_follower(item['id']))


            return data
        else:
            return followeds


    def get_serializer(self, *args,**kwargs):
        print(self.get_queryset())
        return MySerializer(self.get_queryset(),many=True)









from posts.serializers import PostSerializer

from posts.models import Post
class MyDynamicVIew(ListAPIView):

    """ 返回用户的文章列表"""
    serializer_class =PostSerializer


    def get_queryset(self):

        print(self.kwargs["pk"])
        return Post.objects.filter(author_id=self.kwargs["pk"])


class FollowedsPostsVIew(ListAPIView):

    """ 返回用户的文章列表"""
    serializer_class =PostSerializer


    def get_queryset(self):

        print(self.kwargs["pk"])
        user_list = FriendShip.user_followed(self.kwargs['pk'])
        print("那个用户", self.kwargs["pk"])

        print("关注", user_list)


        return Post.objects.filter(author__in=user_list)









