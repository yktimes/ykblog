from .serializers import *

from .models import User, FriendShip

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
from posts.serializers import PostSerializer,MyCommentSerializer

from posts.models import Post,Comment


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

            return Response({'status': 'ok', 'id': user.pk, 'username': user.username})

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # return self.create(request, *args, **kwargs)


from rest_framework.permissions import IsAuthenticated


class UserViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        # is_following={}
        self.serializer_class = Mysite
        user = request.user

        is_following = FriendShip.is_following(user, self.kwargs['pk'])

        data = self.retrieve(request, *args, **kwargs)

        return Response({'data': data.data, 'is_following': is_following})

    def put(self, request, *args, **kwargs):
        # TODO 设置 permission_classes 开启

        print("1111", self.kwargs["pk"])
        print(request.data)
        # users/(?P<pk>\d+)/  self.kwargs["pk"] 得到URLpk
        user = request.user
        print(user.pk)
        if int(request.user.pk) == int(self.kwargs["pk"]):


            serializer = UserUpdatev2Serializer(data=request.data)
            if serializer.is_valid():

                user.name = serializer.data['name']
                user.location = serializer.data['location']
                user.about_me = serializer.data['about_me']
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

        print(11111111111, user, to_user)

        try:

            to_use = User.objects.get(pk=to_user)
            FriendShip.unfollow(user, to_use)


        except:
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'ok', 'status': 'success'}, status=status.HTTP_200_OK)


class FollowView(APIView):
    """
    关注
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        print("关注")

        to_user = int(self.kwargs["pk"])

        user = request.user

        try:
            to_user = User.objects.get(pk=to_user)
            FriendShip.follow(user, to_user)


        except:
            return Response({'message': 'error', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'success'}, status=status.HTTP_200_OK)


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
        if len(followers) > 0:
            id = [i.pk for i in followers]
            data = User.objects.filter(id__in=id).values("id", "username", "name", "email", "avatar")
            print(FollowerView)
            print(data)
            # 为每个 follower 添加 其他属性
            for item in data:
                item['is_following'] = FriendShip.is_following(pk, item['id'], )
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

        if len(followeds) > 0:
            id = [i.pk for i in followeds]
            data = User.objects.filter(id__in=id).values("id", "username", "name", "email", "avatar")

            print("FollowedView")
            # 为每个 follower 添加 其他属性
            for item in data:
                item['is_following'] = FriendShip.is_following(pk, item['id'])
                # 注意细节
                item['date'] = FriendShip.objects.get(followed=item['id'], follower=pk).date
                item['followeds_count'] = len(FriendShip.user_followed(item['id']))
                item['followers_count'] = len(FriendShip.user_follower(item['id']))

            return data
        else:
            return followeds

    def get_serializer(self, *args, **kwargs):
        print(self.get_queryset())
        return MySerializer(self.get_queryset(), many=True)




class MyDynamicVIew(ListAPIView):
    """ 返回用户的文章列表"""
    serializer_class = PostSerializer

    def get_queryset(self):
        print(self.kwargs["pk"])
        return Post.objects.filter(author_id=self.kwargs["pk"])


class FollowedsPostsVIew(ListAPIView):
    """ 返回用户的文章列表"""
    serializer_class = PostSerializer

    def get_queryset(self):
        print(self.kwargs["pk"])
        user_list = FriendShip.user_followed(self.kwargs['pk'])

        return Post.objects.filter(author__in=user_list)


from django.db.models import Q
from ykblog.utils.pagination import StandardResultPagination


class UserReceivedCommentsVIew(APIView):

    def get(self,request,pk):
        try:
            real_user = User.objects.get(id=pk)

            page = int(request.query_params["page"])
            per_page = int(request.query_params["per_page"])

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user!=real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            else:

                # 创建分页对象,继承
                pg = StandardResultPagination()

                # 用户发布的所有文章ID集合
                user_posts_ids=[post.id for post in Post.objects.filter(author=user.pk).all()]
                print("评论，",user_posts_ids)
                # 评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）

                data = Comment.objects.filter(Q(post__in=user_posts_ids)&(~Q(author=user))).order_by('mark_read','-timestamp')


                print("page",page)
                print("per_page",per_page)

                print("data",data)
                res = MyCommentSerializer(instance=data, many=True)
                res = res.data
                # todo 如果没用要删除
                # 标记哪些评论是新的
                last_read_time = user.last_recived_comments_read_time or datetime.datetime(1900, 1, 1)
                for item in res:
                    # print(item["timestamp"])
                    # print(last_read_time)
                    # print(type(item["timestamp"]))
                    # print(type(str(last_read_time)))
                    if item["timestamp"] > str(last_read_time):
                        item["is_new"] = True
                        print(111111111111)
                    print(item)

                # 需要考虑分页的问题，比如新评论有25条，默认分页是每页10条，
                # # 如果用户请求第一页时就更新 last_recived_comments_read_time，那么后15条就被认为不是新评论了，这是不对的
                if page*per_page >= user.new_recived_comments():
                    # 更新 last_recived_comments_read_time 属性值
                    user.last_recived_comments_read_time = datetime.datetime.utcnow()
                    # 将新评论通知的计数归零
                    user.add_notification('unread_recived_comments_count', 0)

                else:
                    # 用户剩余未查看的新评论数
                    n = user.new_recived_comments() - page* per_page
                    # 将新评论通知的计数更新为未读数
                    user.add_notification('unread_recived_comments_count', n)


                user.save()

                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                s = pg.get_paginated_response(data=ret)

                return s


class UserCommentsVIew(APIView):

    def get(self,request,pk):
        try:
            real_user = User.objects.get(id=pk)

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user!=real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            else:

                # 创建分页对象,继承
                pg = StandardResultPagination()



                # 用户发布的所有文章ID集合
                user_posts_ids=[post.id for post in Post.objects.filter(author=user.pk).all()]
                print("评论，",user_posts_ids)
                # 评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）

                data = Comment.objects.filter(post__in=user_posts_ids,author=user).order_by('mark_read','-timestamp')


                print("data",data)
                res = MyCommentSerializer(instance=data, many=True)
                res = res.data


                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                s = pg.get_paginated_response(data=ret)

                return s