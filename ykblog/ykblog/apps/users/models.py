from django.db import models

# Create your models here.
from  django.contrib.auth.models import AbstractUser
import datetime

# from posts.models import Post
from posts.models import Comment
from notification.models import Notification

from django.db.models import Q

import json

class User(AbstractUser):
    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')


    name = models.CharField(max_length=30,default='')
    location = models.CharField(max_length=50,default='')
    about_me = models.CharField(max_length=255,default='')
    avatar=models.CharField(max_length=255,default='')
    # 用户最后一次查看 收到的评论 页面的时间，用来判断哪些收到的评论是新的
    last_recived_comments_read_time = models.DateTimeField(null=True,blank=True,auto_now_add=True)


    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def new_recived_comments(self):
        '''用户发布的文章下面收到的新评论计数'''
        last_read_time = self.last_recived_comments_read_time or datetime.datetime(1900, 1, 1)
        # 用户发布的所有文章 # 反向关联
        user_posts_ids = [post.id for post in self.posts.all()]
        # 用户收到的所有评论，即评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）
        recived_comments = Comment.objects.filter(Q(post__in=user_posts_ids)& Q(author = self)).order_by(
            "mark_read","-timestamp").filter(timestamp__gt=  last_read_time).count()
        # 新评论
        print("sdfsf",recived_comments)
        return recived_comments

    def add_notification(self, name, data):
        '''给用户实例对象增加通知'''
        # 如果具有相同名称的通知已存在，则先删除该通知
        try:

            notic = self.notifications.get(name=name)

        except :

            n = Notification.objects.create(name=name, payload_json=json.dumps(data), user=self)

            return n
        else:
            notic.delete()
            n = Notification.objects.create(name=name, payload_json=json.dumps(data), user=self)

            return n




class FriendShip(models.Model):
    """
    关注关系表
# followeds 是该用户关注了哪些用户列表
    # followers 是该用户的粉丝列表
    """

    follower = models.ForeignKey(User, related_name='followerd', on_delete=models.CASCADE)  # 被别人关注

    followed = models.ForeignKey(User, related_name='followedd',on_delete=models.CASCADE)  # 关注别人


    date = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ('-date',)


    def __str__(self):
        return f'{self.follower} follow {self.followed}'

    # @property
    # def followed_posts(self):
    #     '''获取当前用户的关注者的所有文章列表'''
    #     followed = Post.objects.filter(author=self.followed)
    #     # 包含当前用户自己的文章列表
    #     # own = Post.query.filter_by(user_id=self.id)
    #     # return followed.union(own).order_by(Post.timestamp.desc())
    #     return followed


    @staticmethod
    def is_following(from_user,to_user):
        return  FriendShip.objects.filter(follower=from_user, followed=to_user).count()>0

    @staticmethod
    def follow(from_user, to_user):
        FriendShip(follower=from_user,
                   followed=to_user).save()  # 关注

    @staticmethod
    def unfollow(from_user, to_user):
        f = FriendShip.objects.filter(follower=from_user, followed=to_user).all()
        print(f)
        if f:
            f.delete()  # 取关

    @staticmethod
    def user_followed(from_user):
        """
        得到该用户关注了哪些用户列表
        :param from_user:
        :return:
        """
        # followeds 是该用户关注了哪些用户列表

        # followers 是该用户的粉丝列表
        followeders = FriendShip.objects.filter(follower=from_user).all()

        user_followed = []
        for followeder in followeders:
            user_followed.append(followeder.followed)
        return user_followed  # 得到from_user关注的人，返回列表

    @staticmethod
    def user_follower(from_user):
        """
        得到该用户的粉丝列表
        :param from_user:
        :return:
        """
        # followeds 是该用户关注了哪些用户列表
        # followers 是该用户的粉丝列表
        print(111111111111)
        followeders = FriendShip.objects.filter(followed=from_user).all()
        print("fff", followeders)
        user_followed = []
        for followeder in followeders:
            user_followed.append(followeder.follower)
        return user_followed  # 得到关注我的人，返回列表
