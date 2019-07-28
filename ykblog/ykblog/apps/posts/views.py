from django.shortcuts import render
from .models import Post, Comment
# Create your views here.
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)

from rest_framework.response import Response
from .serializers import PostSerializer, CreateWallCommentSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, ListAPIView
from django.db.models import F

from ykblog.utils.pagination import StandardResultPagination


class PostViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    # queryset和serializer_class是固定写法
    queryset = Post.objects.all().select_related('author')
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
            title = serializer.data.get('title')
            body = serializer.data.get('body')
            summary = serializer.data.get('summary')
            author = request.user

            print("sssssss", summary)
            post = Post.objects.create(title=title, body=body, summary=summary, author=author)

            return Response({'status': 'ok', 'id': post.pk, 'title': post.title, })

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # return self.create(request, *args, **kwargs)


from rest_framework.permissions import IsAuthenticated


class PostViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.views=F("views") + 1
        instance.save()

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


class CommentsView(ListModelMixin, GenericAPIView):
    # queryset和serializer_class是固定写法
    queryset = Comment.objects.all().select_related('author', 'parent', 'post')
    serializer_class = CreateWallCommentSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)

        body = request.data.get('body').strip()
        post = request.data.get('post')

        parent = request.data.get('parent_id')
        print(body, post)

        if not all([body, post]):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:

            post = Post.objects.get(id=int(post))
            print(post, "成功")
        except Post.DoexNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        else:
            if parent:
                try:
                    parent = Comment.objects.get(id=int(parent))
                    Comment.objects.create(author=request.user, body=body, post=post, parent=parent)


                    print(parent, "成功")
                except Comment.DoexNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                print("11111111111", post.comments_count)
                post.comments_count = F("comments_count") + 1
                post.save()
                Comment.objects.create(author=request.user, body=body, post=post)

            # 给文章作者发送新评论通知
            post.author.add_notification('unread_recived_comments_count',
                                         post.author.new_recived_comments())

            return Response(status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentsViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Comment.objects.all().select_related('author', 'parent', 'post')
    serializer_class = CreateWallCommentSerializer

    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)

    @permission_classes((IsAuthenticated,))
    def put(self, request, *args, **kwargs):
        # TODO 设置 permission_classes 开启
        instance = self.get_object()


        flag = request.data.get('disabled')
        mark_read=request.data.get('mark_read')
        print("flag",flag,type(flag))
        print("mark_read",mark_read,type(mark_read))
        # 如果请求用户是该评论用户或着它是该博客主人
        if int(request.user.pk) == int(instance.author.pk) or int(request.user.pk) == int(instance.post.author.pk):

            try:
                c = Comment.objects.get(pk=self.kwargs['pk'])
            except Comment.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                if mark_read is not None:
                    c.mark_read=True
                    c.save()
                if flag is not None:
                    c.disabled = flag
                    c.save()
                return Response(status=status.HTTP_200_OK)

    @permission_classes((IsAuthenticated,))
    def delete(self, request, *args, **kwargs):
        # 如果请求用户是该评论用户或着它是该博客主人

        instance = self.get_object()

        if int(request.user.pk) == int(instance.author.pk) or int(request.user.pk) == int(instance.post.author.pk):
            instance.delete()
            # 给文章作者发送新评论通知(需要自动减1)
            instance.post.author.add_notification('unread_recived_comments_count',
                                         instance.post.author.new_recived_comments())
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


# / api / posts / 1 / comments /?page = 1 & per_page = 10 /
# class PostCommentView1(APIView):
#
#
#
#     def get(self,request,pk,*args, **kwargs):
#
#
#
#         pk = pk
#         try:
#             post = Post.objects.get(pk=pk)
#         except Post.DoesNotExist as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         else:
#             # 获取所有数据
#             # comment_list=Comment.objects.filter(post=pk).values()
#             c = Comment.objects.filter(post=pk)
#             # 创建分页对象
#             pg = PageNumberPagination()
#
#
#             res = CommentSerializer(instance=c,many=True)
#             res = res.data
#
#
#
#             ret = []  # 最终拿到的数据
#             comment_list_dict = {}  # 构建的中间字典
#             #for row in comment_list:  # 通过查到的数据中的id作为key，每一行数据作为value生成一个字典
#             for row in res:  # 通过查到的数据中的id作为key，每一行数据作为value生成一个字典
#                 row.update({"child": []})  # 构建一个键children对应一个空列表
#                 comment_list_dict[row["id"]] = row  # 将id作为键，当前行作为值存到该字典中
#             # print(comment_list_dict)
#
#             for item in res:  # 遍历一遍取到的数据列表
#                 # print("item....",item['parent'])
#                 parrent_row = item["parent"]  # 拿到当前行对应的父亲的地址
#                 if not parrent_row:  # 如果父亲是None，则直接进入ret中
#                     ret.append(item)
#                 else:  # 否则，将这行append到父亲的children中
#
#                     comment_list_dict[parrent_row]["child"].append(item)  # 重点在这一行，用到了上面提到的第一个知识点
#
#             ret = pg.paginate_queryset(queryset=ret, request=request, view=self)
#
#             # print('222222222',ret)
#             # ret = pg.get_paginated_response(ret)
#             s = pg.get_paginated_response(data=ret)
#
#             return s

class PostCommentView(APIView):

    def get(self, request, pk, *args, **kwargs):

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            # 获取所有数据

            # TODO .order_by('timestamp')
            c = Comment.objects.filter(post=pk, parent=None).select_related('author', 'parent', 'post')
            # 创建分页对象,继承
            pg = StandardResultPagination()

            res = CommentSerializer(instance=c, many=True)
            res = res.data

            # 再添加子孙到一级评论的 child 属性上
            for item in res:
                comment = Comment.objects.get(pk=item['id'])

                d = [CommentSerializer(instance=child).data for child in comment.get_descendants()]
                # 按 timestamp 排序一个字典列表
                from operator import itemgetter
                item['child'] = sorted(d, key=itemgetter('timestamp'))

            ret = pg.paginate_queryset(queryset=res, request=request, view=self)

            s = pg.get_paginated_response(data=ret)

            return s

class LikeView(APIView):
    """点赞"""
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        """点赞功能"""

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:

            # 取消或添加赞
            comment.switch_like(request.user)
            # news.update(up_count=F("up_count") + 1)

            # return Response({"likes": news.count_likers()})
            return Response({'status': 'success'},status=status.HTTP_200_OK)
