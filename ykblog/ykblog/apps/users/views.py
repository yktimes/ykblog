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
from posts.serializers import PostSerializer, MyCommentSerializer, LikedCommentSerializer, UserPostInfo

from posts.models import Post, Comment
from .serializers import LiedSerializers


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
        print("关注")

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
        page = int(self.request.query_params["page"])
        per_page = int(self.request.query_params["per_page"])

        user = self.request.user
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

                # 标记哪些粉丝是新的
                last_read_time = user.last_follows_read_time or datetime.datetime(1900, 1, 1)
                for item in data:

                    if item["date"] > last_read_time:
                        print("新的", )
                        item["is_new"] = True

                # 需要考虑分页的问题，比如新评论有25条，默认分页是每页10条，
                # # 如果用户请求第一页时就更新 last_recived_comments_read_time，那么后15条就被认为不是新评论了，这是不对的
                if page * per_page >= user.new_recived_comments():
                    # 更新 last_recived_comments_read_time 属性值
                    user.last_follows_read_time = datetime.datetime.now()
                    # 将新粉丝通知的计数归零
                    user.add_notification('unread_follows_count', 0)

                else:
                    # 用户剩余未查看的新粉丝数
                    n = user.new_recived_comments() - page * per_page
                    # 将新粉丝通知的计数更新为未读数
                    user.add_notification('unread_follows_count', n)

                user.save()

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
        user_list = FriendShip.user_followed(self.kwargs['pk'])

        return Post.objects.filter(author__in=user_list)


from django.db.models import Q
from ykblog.utils.pagination import StandardResultPagination


class UserReceivedCommentsVIew(APIView):
    """
    通知里的评论
    """

    def get(self, request, pk):
        try:
            real_user = User.objects.get(id=pk)

            page = int(request.query_params["page"])
            per_page = int(request.query_params["per_page"])

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
                user_posts_ids = [post.id for post in Post.objects.filter(author=user.pk).all()]

                # 评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）

                q1 = Comment.objects.filter(Q(post__in=user_posts_ids) & (~Q(author=user)))

                descendants = set()

                for c in user.comments.all():
                    descendants = descendants | c.get_descendants()
                descendants = descendants - set(user.comments.all())  # 除去自己在底下回复的
                descendants_ids = [c.id for c in descendants]
                q2 = Comment.objects.filter(id__in=descendants_ids)
                data = q1.union(q2).order_by('mark_read', '-timestamp')

                res = MyCommentSerializer(instance=data, many=True)
                res = res.data
                # todo 如果没用要删除
                # 标记哪些评论是新的
                last_read_time = user.last_recived_comments_read_time or datetime.datetime(1900, 1, 1)
                for item in res:

                    if item["timestamp"] > str(last_read_time):
                        item["is_new"] = True

                # 需要考虑分页的问题，比如新评论有25条，默认分页是每页10条，
                # # 如果用户请求第一页时就更新 last_recived_comments_read_time，那么后15条就被认为不是新评论了，这是不对的
                if page * per_page >= user.new_recived_comments():
                    # 更新 last_recived_comments_read_time 属性值
                    user.last_recived_comments_read_time = datetime.datetime.now()
                    # 将新评论通知的计数归零
                    user.add_notification('unread_recived_comments_count', 0)

                else:
                    # 用户剩余未查看的新评论数
                    n = user.new_recived_comments() - page * per_page
                    # 将新评论通知的计数更新为未读数
                    user.add_notification('unread_recived_comments_count', n)

                user.save()

                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                s = pg.get_paginated_response(data=ret)

                return s


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

                data = user.comments.all().order_by('-timestamp')

                res = MyCommentSerializer(instance=data, many=True)
                res = res.data

                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                s = pg.get_paginated_response(data=ret)

                return s


from operator import itemgetter
from posts.models import Likedship


class UserReceivedLikesVIew(APIView):
    def get(self, request, pk):

        print("点赞")

        try:
            real_user = User.objects.get(id=pk)

            page = int(request.query_params["page"])
            per_page = int(request.query_params["per_page"])

        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            else:
                records = {'items': []}
                # 创建分页对象,继承
                pg = StandardResultPagination()

                # 用户发布的所有文章ID集合
                # comments = user.comments.filter(liked=)
                # from django.db import connection
                #
                # cursor = connection.cursor()
                #
                # cursor.execute('select * from posts_comment_liked,posts_comment where posts_comment.id=comment_id')
                #
                # ret = cursor.fetchall()
                # for c in ret:
                #     print(c)
                # print("ssss",len(ret))
                # origin = user.comments.all().values("liked__comment",'liked')
                # # {'id': 1, 'liked__id': 1, 'body': 'asas'}
                # print(origin)
                # comment_ids =[i['liked__comment'] for i in origin if i['liked__comment']]
                # user_ids = [j['liked'] for j in origin if j['liked']]
                # # timestamps = [t['likedship__timestamp'] for t in origin]
                # comments = Comment.objects.filter(id__in=comment_ids)
                #
                # users = User.objects.filter(id__in=user_ids)
                # print("comments",comments)
                print("ccccc",user.comments.all())
                from django.db import connection

                cursor = connection.cursor()

                cursor.execute(
                    'select posts_likedship.comment_id,posts_likedship.user_id from posts_comment,posts_likedship where posts_comment.id=posts_likedship.comment_id and posts_comment.author_id =%s', [user.pk])

                ret = cursor.fetchall()
                print("ret1111111111", ret)
                from posts.models import Likedship
                k = []
                for r in ret:
                    k.append(Likedship.objects.get(comment=r[0], user=r[1]))

                res = LiedSerializers(k, many=True).data
                print("rrsd",res)
                # todo 如果没用要删除
                # 标记哪些评论是新的
                last_read_time = user.last_likes_read_time or datetime.datetime(1900, 1,
                                                                                           1)
                for item in res:  # data={}
                    #     for u in UserPostInfo(users,many=True).data:
                    if item["timestamp"] > str(last_read_time):  #
                        item["is_new"] = True
                # 按 timestamp 排序一个字典列表(倒序，最新关注的人在最前面)
                res = sorted(res, key=itemgetter('timestamp'), reverse=True)
                print("res",res)
                # 需要考虑分页的问题，比如新评论有25条，默认分页是每页10条，
                # # 如果用户请求第一页时就更新 last_recived_comments_read_time，那么后15条就被认为不是新评论了，这是不对的
                if page * per_page >= user.new_likes():
                    # 更新 last_recived_comments_read_time 属性值
                    user.last_likes_read_time = datetime.datetime.now()
                    # 将新评论通知的计数归零
                    user.add_notification('unread_likes_count',
                                          0)
                    #
                else:  # if data['timestamp'] > last_read_time:
                    # 用户剩余未查看的新评论数
                    n = user.new_likes() - page * per_page  # data['is_new'] = True
                    # 将新评论通知的计数更新为未读数
                    user.add_notification('unread_likes_count', n)


                user.save()
                ret = pg.paginate_queryset(queryset=res, request=request, view=self)

                s = pg.get_paginated_response(data=ret)  # 需要                                                                                          考虑分页的问题，比如新评论有25条，默认分页是每页10条，
                # #
                print("ssssssssss",s)

                return s
from Message.models import Message
from Message.serializers import CreateMessageSerializer

class GetUserMessagesSenders(APIView):
    """
      '''哪些用户给我发过私信，按用户分组，返回各用户最后一次发送的私信
    即: (谁) 最后一次 给我发了 (什么私信)'

    """

    def get(self, request, pk):

        try:
            real_user = User.objects.get(id=int(pk))
            page = int(request.query_params["page"])
            per_page = int(request.query_params["per_page"])
        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # 创建分页对象,继承
            pg = StandardResultPagination()
            from django.db.models import Count
            origin_data = user.messages_received.all().values("sender").annotate(total_count=Count("id"))
            print(origin_data)
            reids = [id['sender'] for id in origin_data]
            total_count = [id['total_count'] for id in origin_data]

            print("yyy", total_count)
            # Message.objects.values("recipients").annotate(c=Count("recipients"))
            # 我给每个用户发的私信，他们有没有未读的
            print('sender', reids)

            # data = Message.objects.filter(recipients__in=reids)
            #
            #
            # for item in  data:
            #     print("item",item)

            # print("datadata",data)
            res = []
            for i in range(len(reids)):
                data = CreateMessageSerializer(instance=Message.objects.filter(sender=reids[i]).last()).data
                print(data)
                print('uuu', i)
                # 发给了谁
                sender = User.objects.get(id=reids[i])
                print(sender)
                # 总共给他发过多少条

                data['total_count'] = int(total_count[i])
                # 他最后一次查看收到的私信的时间

                # print(22222222222222222)
                # # 他最后一次查看收到的私信的时间
                last_read_time = sender.last_messages_read_time or datetime.datetime(1900, 1, 1)
                print(11111111111111111111111111)
                new_items = []  # 最后一条是新的
                not_new_items = []  # 最后一条不是新的
                # item 是发给他的最后一条，如果最后一条不是新的，肯定就没有啦
                if data['timestamp'] > str(last_read_time):
                    data['is_new'] = True
                    # 继续获取发给这个用户的私信有几条是新的
                    data['new_count'] = Message.objects.filter(sender=reids[i]).filter(
                        timestamp__gt=last_read_time).count()
                    new_items.append(data)
                else:
                    not_new_items.append(data)


                res.append(data)
            # res =
            # res = res.data

            print("哪些用户geiwo发过私信", res)
            ret = pg.paginate_queryset(queryset=res, request=request, view=self)

            s = pg.get_paginated_response(data=ret)

            return s


class GetUserListMessagesRecipients(APIView):
    '''我给哪些用户发过私信，按用户分组，返回我给各用户最后一次发送的私信
    即: 我给 (谁) 最后一次 发了 (什么私信)'''

    def get(self,request,pk):


        try:
            real_user = User.objects.get(id=int(pk))
            page = int(request.query_params["page"])
            per_page = int(request.query_params["per_page"])
        except User.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user != real_user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # 创建分页对象,继承
            pg = StandardResultPagination()
            from django.db.models import  Count
            origin_data = user.messages_sent.all().values("recipient").annotate(total_count=Count("id"))
            print(origin_data)
            reids = [id['recipient'] for id in origin_data]
            total_count = [id['total_count'] for id in origin_data]

            print("yyy",total_count)
            # Message.objects.values("recipients").annotate(c=Count("recipients"))
            # 我给每个用户发的私信，他们有没有未读的
            print('reids',reids)



            # data = Message.objects.filter(recipients__in=reids)
            #
            #
            # for item in  data:
            #     print("item",item)

            # print("datadata",data)
            res=[]
            for i in range(len(reids)):
                data = CreateMessageSerializer(instance=Message.objects.filter(recipient=reids[i]).last()).data
                print(data)
                print('uuu',i)
                # 发给了谁
                recipient = User.objects.get(id =reids[i])
                print(recipient)
                # 总共给他发过多少条

                data['total_count'] = int(total_count[i])
        # 他最后一次查看收到的私信的时间

                # print(22222222222222222)
                # # 他最后一次查看收到的私信的时间
                last_read_time = recipient.last_messages_read_time or datetime.datetime(1900, 1, 1)
                print(11111111111111111111111111)
                # item 是发给他的最后一条，如果最后一条不是新的，肯定就没有啦
                if data['timestamp'] > str(last_read_time):
                    data['is_new'] = True
                    # 继续获取发给这个用户的私信有几条是新的
                    data['new_count'] = Message.objects.filter(recipient=reids[i]).filter(
                        timestamp__gt=last_read_time).count()
                res.append(data)
            # res =
            # res = res.data

            print("我给哪些用户发过私信",res)
            ret = pg.paginate_queryset(queryset=res, request=request, view=self)

            s = pg.get_paginated_response(data=ret)

            return s

class GetUserHistoryMessages(APIView):
    '''返回我与某个用户(由查询参数 from 获取)之间的所有私信记录'''
    def get(self,request,pk):

        try:
            real_user = User.objects.get(id=int(pk))
            page = int(request.query_params["page"])
            per_page = int(request.query_params["per_page"])
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
            print(from_id)
            # 对方发给我的
            q1 = Message.objects.filter(sender= from_id, recipient = pk).select_related('sender','recipient')
            # 我发给对方的
            q2 = Message.objects.filter(sender= pk, recipient= from_id).select_related('sender','recipient')

            # 按时间正序排列构成完整的对话时间线
            history_messages = q1.union(q2).order_by('timestamp')
            data = CreateMessageSerializer(history_messages,many=True).data
            # 现在这一页的 data['items'] 包含对方发给我和我发给对方的
            # 需要创建一个新列表，只包含对方发给我的，用来查看哪些私信是新的
            recived_messages = [item for item in data if item['sender']['id'] != id]
            sent_messages = [item for item in data  if item['sender']['id'] == id]
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
                user.add_notification('unread_messages_count', user.new_recived_messages())
                user.save()
            # 最后，重新组合 data['items']，因为收到的新私信添加了 is_new 标记
            messages = recived_messages + sent_messages
            messages.sort(key=data.index)  # 保持 messages 列表元素的顺序跟 data['items'] 一样
            print("我给哪些用户发过私信", data)
            ret = pg.paginate_queryset(queryset=data, request=request, view=self)

            s = pg.get_paginated_response(data=ret)

            return s