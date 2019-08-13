from django.db import models

# Create your models here.
from  django.contrib.auth.models import AbstractUser
import datetime
from django.conf import settings
# from posts.models import Post
from posts.models import Comment
from notification.models import Notification

from django.db.models import Q

import json
from posts.models import Likedship,LikedPost
from Message.models import Message



# from ykblog.utils.tasks import send_messages

# from rq_tasks.tasks import send_messages
class User(AbstractUser):
    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')


    name = models.CharField(max_length=30,default='')
    location = models.CharField(max_length=50,default='')
    about_me = models.CharField(max_length=255,default='')
    avatar=models.CharField(max_length=255,default='')

    harassers  = models.ManyToManyField('users.User', through='Blacklist',
                                   through_fields=('user', 'block'), verbose_name='黑名单用户')

    # 用户最后一次查看 收到的评论 页面的时间，用来判断哪些收到的评论是新的
    last_recived_comments_read_time = models.DateTimeField(null=True,blank=True)

    # 用户最后一次查看 用户的粉丝 页面的时间，用来判断哪些粉丝是新的
    last_follows_read_time = models.DateTimeField(null=True,blank=True)
    # 用户最后一次查看 收到的点赞 页面的时间，用来判断哪些点赞是新的
    last_comments_likes_read_time  = models.DateTimeField(null=True,blank=True)

    # 用户最后一次查看私信的时间
    last_messages_read_time = models.DateTimeField(null=True,blank=True)

    # 用户最后一次查看 收到的文章被喜欢 页面的时间，用来判断哪些喜欢是新的
    last_posts_likes_read_time = models.DateTimeField(null=True,blank=True)


    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name



    def launch_task(self, name, description, *args, **kwargs):
        '''用户启动一个新的后台任务'''

        print('''用户启动一个新的后台任务''')
        # 创建一个进程调用发送短信的函数
        from celery_tasks.message.tasks import send_messages

        celery_job = send_messages.delay(*args,**kwargs)
        print(celery_job)



    def new_posts_likes(self):
        '''用户收到的文章被喜欢的新计数'''

        last_read_time = self.last_posts_likes_read_time or datetime.datetime(1900, 1, 1)
        # 当前用户发表的所有评论当中，哪些被点赞了
        from django.db import connection

        cursor = connection.cursor()

        cursor.execute(
            'select posts_likedpost.post_id,posts_likedpost.user_id from tb_posts,posts_likedpost where tb_posts.id=posts_likedpost.post_id and tb_posts.author_id =%s',
            [self.pk])

        ret = cursor.fetchall()

        # 新的点赞记录计数
        new_likes_count = 0

        for c in ret:

            if c[1]!=self.pk:

                timestamp = LikedPost.objects.get(user=c[1], post=c[0]).timestamp

                # 判断本条点赞记录是否为新的
                if timestamp > last_read_time:
                    new_likes_count += 1

        return new_likes_count



    def is_blocking(self, user):

        return user in self.harassers.all()
            #
            # self.harassers.all().filter(
            # block = user.id).count() > 0

    def block(self, user):
        '''当前用户开始拉黑 user 这个用户对象'''
        if not self.is_blocking(user):
            Blacklist.objects.create(user=self,block=user)
            # self.harassers.append(user)

    def unblock(self, user):
        '''当前用户取消拉黑 user 这个用户对象'''
        if self.is_blocking(user):
            Blacklist.objects.get(user=self, block=user).delete()
            # self.harassers.remove(user)


    def new_recived_messages(self):
        '''用户未读的私信计数'''
        last_read_time = self.last_messages_read_time or datetime.datetime(1900, 1, 1)


        return Message.objects.filter(recipient=self).filter(
            timestamp__gt= last_read_time).count()

    def new_recived_comments(self):
        '''用户发布的文章下面收到的新评论计数'''
        last_read_time = self.last_recived_comments_read_time or datetime.datetime(1900, 1, 1)

        # 用户发布的所有文章 # 反向关联
        user_posts_ids = [post.id for post in self.posts.all()]

        # 用户收到的所有评论，即评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）
        recived_comments = Comment.objects.filter(Q(post__in=user_posts_ids)& ~Q(author = self)).filter(timestamp__gt=  last_read_time).count()

        # 用户文章下面的新评论, 即评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是自己(文章的作者)
        q1 = set(Comment.objects.filter(Q(post__in=user_posts_ids)& ~Q(author = self)))

        # 用户发表的评论被人回复了，找到每个用户评论的所有子孙
        q2 = set()
        for c in self.comments.all():

            q2 = q2 | c.get_descendants()
        q2 = q2 - set(self.comments.all())  # 除去子孙中，用户自己发的(因为是多级评论，用户可能还会在子孙中盖楼)，自己回复的不用通知
        # 用户收到的总评论集合为 q1 与 q2 的并集
        recived_comments = q1 | q2
        #最后，再过滤掉 last_read_time 之前的评论

        l =  len([c for c in recived_comments if c.timestamp > last_read_time])

        return l





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

    def new_follows(self):
        '''用户的新粉丝计数'''
        last_read_time = self.last_follows_read_time or datetime.datetime(1900, 1, 1)


        s = self.followedd.filter(date__gt=last_read_time).count()


        return s

    def new_comments_likes(self):
        '''用户收到的新点赞计数'''
        last_read_time = self.last_comments_likes_read_time  or datetime.datetime(1900, 1, 1)
        # 当前用户发表的所有评论当中，哪些被点赞了
        from django.db import connection

        cursor = connection.cursor()

        cursor.execute('select posts_likedship.comment_id,posts_likedship.user_id from posts_comment,posts_likedship where posts_comment.id=posts_likedship.comment_id and posts_comment.author_id =%s', [self.pk])


        ret = cursor.fetchall()

        # 新的点赞记录计数
        new_likes_count = 0

        for c in ret:
            print(c)
            timestamp = Likedship.objects.get(user=c[1], comment=c[0]).timestamp
            print("事件",timestamp)
            # 判断本条点赞记录是否为新的
            if timestamp > last_read_time:
                new_likes_count += 1
        print("new_likes_count",new_likes_count)
        return new_likes_count



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

        followeders = FriendShip.objects.filter(followed=from_user).all()

        user_followed = []
        for followeder in followeders:
            user_followed.append(followeder.follower)
        return user_followed  # 得到关注我的人，返回列表


class Blacklist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='harasser',on_delete=models.CASCADE)

    # 这个是黑名单
    block=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sufferer', on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blacklist'
        verbose_name = '黑名单'
        verbose_name_plural = verbose_name


