from django.shortcuts import render
from .models import Post, Comment,Category
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
from .serializers import PostSerializer, CreateWallCommentSerializer, CommentSerializer,PostIndexSerializer,PostLikeMoreSerializer,PostListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, ListAPIView
from django.db.models import F

from ykblog.utils.pagination import StandardResultPagination

from rest_framework.permissions import IsAuthenticated,IsAdminUser

from drf_haystack.viewsets import HaystackViewSet

class PostSearchViewSet(HaystackViewSet):
    """

    """
    index_models = [Post]

    serializer_class = PostIndexSerializer


class PostViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    # queryset和serializer_class是固定写法
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        # self.serializer_class = PostListSerializer
        return self.list(request, *args, **kwargs)

    @permission_classes((IsAdminUser,))
    def post(self, request, *args, **kwargs):


        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            title = serializer.data.get('title')
            body = serializer.data.get('body')
            summary = serializer.data.get('summary')
            author = request.user
            category = serializer.data.get('category')
            image = serializer.data.get('image')


            try:
                c = Category.objects.get(id=category)
            except Category.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            post = Post.objects.create(title=title, body=body, summary=summary, author=author,category=c,image=image)

            return Response({'message': 'ok', 'id': post.pk, 'title': post.title, })

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PostViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.views=F("views") + 1

        instance.save()

        return self.retrieve(request, *args, **kwargs)

    @permission_classes((IsAdminUser,))
    def put(self, request, *args, **kwargs):


        if int(request.user.pk) == int(self.get_object().author.pk):
            return self.update(request, *args, **kwargs)


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

    @permission_classes((IsAuthenticated,))
    def post(self, request, *args, **kwargs):


        body = request.data.get('body').strip()
        post = request.data.get('post')

        parent = request.data.get('parent_id')

        if  len(body.strip())==0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not post:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:

            post = Post.objects.get(id=int(post))

        except Post.DoexNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        else:
            if parent:
                try:
                    parent = Comment.objects.get(id=int(parent))
                    comment = Comment.objects.create(author=request.user, body=body, post=post, parent=parent)



                except Comment.DoexNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:

                post.comments_count = F("comments_count") + 1
                post.save()
                comment = Comment.objects.create(author=request.user, body=body, post=post)
            # 添加评论时:
            # 1. 如果是一级评论，只需要给文章作者发送新评论通知
            # 2. 如果不是一级评论，则需要给文章作者和该评论的所有祖先的作者发送新评论通知
            users = set()
            users.add(comment.post.author)  # 将文章作者添加进集合中
            if comment.parent:
                ancestors_authors = {c.author for c in comment.get_ancestors()}
                users = users | ancestors_authors
            # 给各用户发送新评论通知
            for u in users:
                u.add_notification('unread_recived_comments_count',
                                   u.new_recived_comments())


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



        flag = request.data.get('disabled')
        mark_read=request.data.get('mark_read')


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

        # if int(request.user.pk) == int(instance.author.pk) or int(request.user.pk) == int(instance.post.author.pk):
        # 删除评论时:
        # 1. 如果是一级评论，只需要给文章作者发送新评论通知
        # 2. 如果不是一级评论，则需要给文章作者和该评论的所有祖先的作者发送新评论通知
        users = set()
        users.add(instance.post.author)  # 将文章作者添加进集合中
        if instance.parent:
            ancestors_authors = {c.author for c in instance.get_ancestors()}
            users = users | ancestors_authors

        # 必须先删除该评论，后续给各用户发送通知时，User.new_recived_comments() 才能是更新后的值
        instance.delete()
        # 给各用户发送新评论通知
        for u in users:
            u.add_notification('unread_recived_comments_count',
                               u.new_recived_comments())

        return Response(status=status.HTTP_204_NO_CONTENT)



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
            comment.author.add_notification('unread_comments_likes_count', comment.author.new_comments_likes())

            return Response({'status': 'success'},status=status.HTTP_200_OK)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        """喜欢文章功能"""

        try:
            post = Post.objects.get(pk=pk)

        except Post.DoesNotExist as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = request.user
            post.liked_by(user)
            # 切记要先提交，先添加喜欢记录到数据库，因为 new_posts_likes() 会查询 posts_likes 关联表
            post.likers_count = F("likers_count") + 1
            post.save()

            post.author.add_notification('unread_posts_likes_count',
                                         post.author.new_posts_likes())

            return Response({
                'status': 'success',
                'message': '收藏成功'
            },status=status.HTTP_200_OK)

class UnLikePostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        """取消喜欢文章功能"""

        try:
            post = Post.objects.get(pk=pk)

        except Post.DoesNotExist as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = request.user
            post.unliked_by(user)
            # 切记要先提交，先添加喜欢记录到数据库，因为 new_posts_likes() 会查询 posts_likes 关联表
            if post.likers_count>0:
                post.likers_count = F("likers_count") - 1
                post.save()

                post.author.add_notification('unread_posts_likes_count',
                                         post.author.new_posts_likes())

            return Response({
                'status': 'success',
                'message': '取消收藏成功'
            },status=status.HTTP_200_OK)

from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http.response import JsonResponse
@csrf_exempt
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    print(111111111111,type(file),file)
    # for f in file:
    #     name = f.name
    #     print(name,"name")
    #     print(type(f),f.file)
    #     print()
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        print(111111111111111111111111111111)
        print(fp)
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    print(url)
    return JsonResponse({'url':url})

from django_redis import get_redis_connection


import json
class artViewList(APIView):

    def get(self,request):
        redis_conn = get_redis_connection('likeNum')
        key = 'artViewList'

        if redis_conn.get(key) is None:
            post = Post.objects.all().order_by('-views')[:10]
            data = json.dumps(PostLikeMoreSerializer(post, many=True).data)
            redis_conn.setex(key,60*5,data)

            return Response({
                'data': data,
                'message': 'success'
            }, status=status.HTTP_200_OK)
        else:
            print("走的缓存，aret")
            artList = json.loads(redis_conn.get(key))
            print(artList)


            return Response({
                'data': artList,
                'message': 'success'
            },status=status.HTTP_200_OK)

from .models import  Category

class CategoryListView(APIView):
    """
    帖子首页展示
    """
    # permission_classes = [IsAuthenticated]

    def get(self,request):

        # category_id = self.request.query_params.get("category")
        # if category_id:

        c = Category.objects.all().values()
        print(c)
        return Response({'data':c})


class CategoryPostView(ListAPIView):


        queryset = Post.objects.all()
        serializer_class = PostSerializer



        def filter_queryset(self, queryset):
            category_id = self.request.query_params.get("classId")
            if category_id:
                return Post.objects.filter(category=category_id).select_related("author",'category')


