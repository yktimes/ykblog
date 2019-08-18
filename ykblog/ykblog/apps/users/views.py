import datetime
from operator import itemgetter

from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from posts.serializers import PostSerializer, MyCommentSerializer
from posts.models import Post, Comment
from .serializers import *
from posts.models import LikedPost
from .serializers import LikedPostSerializers
from Message.models import Message
from Message.serializers import CreateMessageSerializer
from ykblog.utils.pagination import StandardResultPagination


class UserViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    """创建用户"""
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


class UserViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):

        self.serializer_class = Mysite
        user = request.user

        is_following = FriendShip.is_following(user, self.kwargs['pk'])

        data = self.retrieve(request, *args, **kwargs)

        return Response({'data': data.data, 'is_following': is_following})

    def put(self, request, *args, **kwargs):
        # TODO 设置 permission_classes 开启

        # users/(?P<pk>\d+)/  self.kwargs["pk"] 得到URLpk
        user = request.user

        if int(request.user.pk) == int(self.kwargs["pk"]):

            serializer = UserUpdatev2Serializer(data=request.data)
            if serializer.is_valid():

                user.name = serializer.data['name']
                user.location = serializer.data['location']
                user.about_me = serializer.data['about_me']
                user.save()

                return Response({'message': 'ok', 'id': user.pk, 'username': user.username})

            else:

                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        # 需要判断

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

        to_user = int(self.kwargs["pk"])

        user = request.user

        try:

            to_user = User.objects.get(pk=to_user)
            FriendShip.unfollow(user, to_user)
            to_user.add_notification('unread_follows_count', to_user.new_follows())


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

        to_user = int(self.kwargs["pk"])

        user = request.user

        try:
            to_user = User.objects.get(pk=to_user)
            FriendShip.follow(user, to_user)
            to_user.add_notification('unread_follows_count', to_user.new_follows())


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

        user = self.request.user
        pk = self.kwargs['pk']
        followers = FriendShip.user_follower(pk)
        if len(followers) > 0:
            id = [i.pk for i in followers]
            data = User.objects.filter(id__in=id).values("id", "username", "name", "email", "avatar")

            # 为每个 follower 添加 其他属性
            for item in data:
                item['is_following'] = FriendShip.is_following(pk, item['id'], )
                # 注意细节
                item['date'] = FriendShip.objects.get(followed=pk, follower=item['id']).date
                item['followeds_count'] = len(FriendShip.user_followed(item['id']))
                item['followers_count'] = len(FriendShip.user_follower(item['id']))

                # 标记哪些粉丝是新的
                last_read_time = user.last_follows_read_time or datetime.datetime(1900, 1, 1)
                for item in data:

                    if item["date"] > last_read_time:
                        item["is_new"] = True

            # 更新 last_recived_comments_read_time 属性值
            user.last_follows_read_time = datetime.datetime.now()
            # 将新粉丝通知的计数归零
            user.add_notification('unread_follows_count', 0)
            user.save()

            return data
        else:
            return followers

    def get_serializer(self, *args, **kwargs):
        return MySerializer(self.get_queryset(), many=True)


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

        return MySerializer(self.get_queryset(), many=True)


class MyDynamicVIew(ListAPIView):
    """ 返回用户的文章列表"""
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related("author").filter(author_id=self.kwargs["pk"])


class FollowedsPostsVIew(ListAPIView):
    """ 返回用户的文章列表"""
    serializer_class = PostSerializer

    def get_queryset(self):
        user_list = FriendShip.user_followed(self.kwargs['pk'])

        return Post.objects.select_related("author").filter(author__in=user_list)


class UserReceivedCommentsVIew(APIView):
    """
    通知里的评论
    """

    def get(self, request, pk):
        try:
            real_user = User.objects.get(id=pk)


        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            else:

                # 创建分页对象,继承
                pg = StandardResultPagination()

                # 用户发布的所有文章ID集合
                user_posts_ids = [post.id for post in Post.objects.select_related("author").filter(author=user.pk).all()]

                # 评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）

                q1 = Comment.objects.select_related('post', 'author').filter(
                    Q(post__in=user_posts_ids) & (~Q(author=user)))

                descendants = set()

                for c in user.comments.all().select_related('post', 'author'):
                    descendants = descendants | c.get_descendants()
                descendants = descendants - set(user.comments.all())  # 除去自己在底下回复的
                descendants_ids = [c.id for c in descendants]
                q2 = Comment.objects.select_related('post', 'author').filter(id__in=descendants_ids)
                data = q1.union(q2).order_by('mark_read', '-timestamp')

                res = MyCommentSerializer(instance=data, many=True)
                res = res.data
                # todo 如果没用要删除
                # 标记哪些评论是新的
                last_read_time = user.last_recived_comments_read_time or datetime.datetime(1900, 1, 1)
                for item in res:

                    if item["timestamp"] > str(last_read_time):
                        item["is_new"] = True

                # 更新 last_recived_comments_read_time 属性值
                user.last_recived_comments_read_time = datetime.datetime.now()
                # 将新评论通知的计数归零
                user.add_notification('unread_recived_comments_count', 0)

                user.save()

                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                return pg.get_paginated_response(data=ret)


class UserCommentsVIew(APIView):
    """
    资源里的评论
    """

    def get(self, request, pk):
        try:
            real_user = User.objects.get(id=pk)

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            else:

                # 创建分页对象,继承
                pg = StandardResultPagination()

                data = user.comments.all().select_related('post', 'author').order_by('-timestamp')

                res = MyCommentSerializer(instance=data, many=True).data

                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                return pg.get_paginated_response(data=ret)


class UserReceivedLikesVIew(APIView):
    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=pk)



        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            else:

                # 创建分页对象,继承
                pg = StandardResultPagination()

                from django.db import connection

                cursor = connection.cursor()

                cursor.execute(
                    'select posts_likedship.comment_id,posts_likedship.user_id from posts_comment,posts_likedship where posts_comment.id=posts_likedship.comment_id and posts_comment.author_id =%s and posts_likedship.user_id!=posts_comment.author_id',
                    [user.pk])

                ret = cursor.fetchall()

                from posts.models import Likedship
                k = []
                for r in ret:
                    k.append(Likedship.objects.get(comment=r[0], user=r[1]))

                res = LiedSerializers(k, many=True).data

                # 标记哪些评论是新的
                last_read_time = user.last_comments_likes_read_time or datetime.datetime(1900, 1, 1)
                for item in res:  # data={}

                    if item["timestamp"] > str(last_read_time):  #
                        item["is_new"] = True
                # 按 timestamp 排序一个字典列表(倒序，最新关注的人在最前面)
                res = sorted(res, key=itemgetter('timestamp'), reverse=True)

                # 更新 last_recived_comments_read_time 属性值
                user.last_comments_likes_read_time = datetime.datetime.now()
                # 将新评论通知的计数归零
                user.add_notification('unread_comments_likes_count', 0)
                user.save()
                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                return pg.get_paginated_response(data=ret)  # 需要


class GetUserMessagesSenders(APIView):
    """
      '''哪些用户给我发过私信，按用户分组，返回各用户最后一次发送的私信
    即: (谁) 最后一次 给我发了 (什么私信)'

    """

    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=int(pk))

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # 创建分页对象,继承
            pg = StandardResultPagination()
            from django.db.models import Count
            origin_data = user.messages_received.all().select_related('sender').values("sender").annotate(
                total_count=Count("id"))

            reids = [id['sender'] for id in origin_data]
            total_count = [id['total_count'] for id in origin_data]

            res = []
            for i in range(len(reids)):
                data = CreateMessageSerializer(
                    instance=Message.objects.select_related('sender').filter(sender=reids[i]).last()).data

                # 发给了谁
                sender = User.objects.get(id=reids[i])

                # 判断我有没有拉黑他
                if user.is_blocking(sender):
                    data['is_blocking'] = True

                # 总共给他发过多少条
                data['total_count'] = int(total_count[i])

                # 他最后一次查看收到的私信的时间
                last_read_time = sender.last_messages_read_time or datetime.datetime(1900, 1, 1)

                new_items = []  # 最后一条是新的
                not_new_items = []  # 最后一条不是新的
                # item 是发给他的最后一条，如果最后一条不是新的，肯定就没有啦
                if data['timestamp'] > str(last_read_time):
                    data['is_new'] = True
                    # 继续获取发给这个用户的私信有几条是新的
                    data['new_count'] = Message.objects.select_related('sender').filter(sender=reids[i]).filter(
                        timestamp__gt=last_read_time).count()
                    new_items.append(data)
                else:
                    not_new_items.append(data)

                res.append(data)

            ret = pg.paginate_queryset(queryset=res, request=request, view=self)

            return pg.get_paginated_response(data=ret)


class GetUserListMessagesRecipients(APIView):
    '''我给哪些用户发过私信，按用户分组，返回我给各用户最后一次发送的私信
    即: 我给 (谁) 最后一次 发了 (什么私信)'''

    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=int(pk))

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # 创建分页对象,继承
            pg = StandardResultPagination()
            from django.db.models import Count
            origin_data = user.messages_sent.all().select_related('recipient').values("recipient").annotate(
                total_count=Count("id"))

            reids = [id['recipient'] for id in origin_data]
            total_count = [id['total_count'] for id in origin_data]

            res = []
            for i in range(len(reids)):
                data = CreateMessageSerializer(instance=Message.objects.select_related("recipient").filter(recipient=reids[i]).last()).data

                # 发给了谁
                recipient = User.objects.get(id=reids[i])

                # 总共给他发过多少条
                data['total_count'] = int(total_count[i])

                # # 他最后一次查看收到的私信的时间
                last_read_time = recipient.last_messages_read_time or datetime.datetime(1900, 1, 1)

                # item 是发给他的最后一条，如果最后一条不是新的，肯定就没有啦
                if data['timestamp'] > str(last_read_time):
                    data['is_new'] = True
                    # 继续获取发给这个用户的私信有几条是新的
                    data['new_count'] = Message.objects.select_related('recipient').filter(recipient=reids[i]).filter(
                        timestamp__gt=last_read_time).count()
                res.append(data)

            ret = pg.paginate_queryset(queryset=res, request=request, view=self)

            return pg.get_paginated_response(data=ret)


class GetUserHistoryMessages(APIView):
    '''返回我与某个用户(由查询参数 from 获取)之间的所有私信记录'''

    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=int(pk))

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # 创建分页对象,继承
            pg = StandardResultPagination()

            from_id = int(request.query_params.get('from'))
            if not from_id:  # 必须提供聊天的对方用户的ID
                return Response(status=status.HTTP_403_FORBIDDEN)

            # 对方发给我的
            q1 = Message.objects.select_related('sender', 'recipient').filter(sender=from_id,
                                                                              recipient=pk).select_related('sender',
                                                                                                           'recipient')
            # 我发给对方的
            q2 = Message.objects.select_related('sender', 'recipient').filter(sender=pk,
                                                                              recipient=from_id).select_related(
                'sender', 'recipient')

            # 按时间正序排列构成完整的对话时间线
            history_messages = q1.union(q2).order_by('timestamp')
            data = CreateMessageSerializer(history_messages, many=True).data
            # 现在这一页的 data['items'] 包含对方发给我和我发给对方的
            # 需要创建一个新列表，只包含对方发给我的，用来查看哪些私信是新的
            recived_messages = [item for item in data if item['sender']['id'] != id]
            sent_messages = [item for item in data if item['sender']['id'] == id]
            # 然后，标记哪些私信是新的
            last_read_time = user.last_messages_read_time or datetime.datetime(1900, 1, 1)

            new_count = 0
            for item in recived_messages:

                if item['timestamp'] > str(last_read_time):
                    item['is_new'] = True
                    new_count += 1

            if new_count > 0:
                # 更新 last_messages_read_time 属性值为收到的私信列表最后一条(最近的)的时间

                user.last_messages_read_time = recived_messages[-1]['timestamp']
            
                user.save()  # 先提交数据库，这样 user.new_recived_messages() 才会变化
                # 更新用户的新私信通知的计数
            user.add_notification('unread_messages_count', 0)
            # user.save()
            # 最后，重新组合 data['items']，因为收到的新私信添加了 is_new 标记
            messages = recived_messages + sent_messages
            messages.sort(key=data.index)  # 保持 messages 列表元素的顺序跟 data['items'] 一样

            ret = pg.paginate_queryset(queryset=data, request=request, view=self)

            s = pg.get_paginated_response(data=ret)

            return s


class BlockView(APIView):
    '''开始拉黑一个用户'''

    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=int(pk))

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user == real_user:
                # 不能拉黑自己
                return Response(status=status.HTTP_403_FORBIDDEN)

            if user.is_blocking(real_user):
                # 已经拉黑了
                return Response(status=status.HTTP_400_BAD_REQUEST)

            user.block(real_user)

            return Response({
                'status': 'success',
                'message': '屏蔽 %s.' % (real_user.name if real_user.name else real_user.username)
            })


class UnBlockView(APIView):
    '''取消拉黑一个用户'''

    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=int(pk))

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user == real_user:
                # 不能拉黑自己
                return Response(status=status.HTTP_403_FORBIDDEN)

            if not user.is_blocking(real_user):
                # 已经拉黑了
                return Response(status=status.HTTP_400_BAD_REQUEST)

            user.unblock(real_user)

            return Response({
                'status': 'success',
                'message': '取消屏蔽 %s.' % (real_user.name if real_user.name else real_user.username)
            })


class UserReceivedPostsLikesVIew(APIView):
    '''返回该用户收到的文章喜欢
    谁喜欢了你的文章
    '''

    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=pk)


        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            else:

                # 创建分页对象,继承
                pg = StandardResultPagination()

                from django.db import connection

                cursor = connection.cursor()

                cursor.execute(
                    'select posts_likedpost.post_id,posts_likedpost.user_id from tb_posts,posts_likedpost where tb_posts.id=posts_likedpost.post_id and tb_posts.author_id =%s and posts_likedpost.user_id!=tb_posts.author_id',
                    [user.pk])

                ret = cursor.fetchall()

                from posts.models import LikedPost
                k = []
                for r in ret:
                    k.append(LikedPost.objects.get(post=r[0], user=r[1]))

                res = LikedPostSerializers(k, many=True).data

                # todo 如果没用要删除
                # 标记哪些文章是新的
                last_read_time = user.last_posts_likes_read_time or datetime.datetime(1900, 1,
                                                                                      1)

                # 重组数据，变成: (谁) (什么时间) 喜欢了你的 (哪篇文章)
                for item in res:  # data={}

                    if item["timestamp"] > str(last_read_time):  #
                        item["is_new"] = True
                # 按 timestamp 排序一个字典列表(倒序，最新关注的人在最前面)
                res = sorted(res, key=itemgetter('timestamp'), reverse=True)

                user.last_posts_likes_read_time = datetime.datetime.now()
                user.add_notification('unread_posts_likes_count', 0)

                user.save()
                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                return pg.get_paginated_response(data=ret)  # 需要


class UserLikesPostsVIew(ListAPIView):

    def get_queryset(self):
        try:

            user = User.objects.get(id=self.kwargs['pk'])


        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            post_list = [p.post.pk for p in LikedPost.objects.select_related('post', 'user').filter(user=user)]

            return Post.objects.select_related('author').filter(id__in=post_list)

    def get_serializer(self, *args, **kwargs):
        return PostSerializer(self.get_queryset(), many=True)
