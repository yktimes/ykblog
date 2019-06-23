from django.db import models

# Create your models here.
from  django.contrib.auth.models import AbstractUser


# from posts.models import Post



class User(AbstractUser):
    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')


    name = models.CharField(max_length=30,default='')
    location = models.CharField(max_length=50,default='')
    about_me = models.CharField(max_length=255,default='')
    avatar=models.CharField(max_length=255,default='')



    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


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
