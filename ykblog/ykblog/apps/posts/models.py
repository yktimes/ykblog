from django.db import models
from django.conf import settings

class Category(models.Model):

    name = models.CharField(max_length=50,verbose_name='名称')

    class Meta:
        verbose_name=verbose_name_plural = '分类'

    def __str__(self):
        return self.name

class Post(models.Model):


    title = models.CharField(max_length=255,verbose_name='标题')
    summary = models.CharField(max_length=255,verbose_name='总结概括')

    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    views =models.IntegerField(default=0)
    image = models.URLField(verbose_name="文章图片")
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='posts',on_delete=models.CASCADE)
    comments_count = models.IntegerField(default=0) # 评论数
    likers_count= models.IntegerField(default=0) # 喜欢数
    # 博客文章与喜欢/收藏它的人是多对多关系
    likers = models.ManyToManyField('users.User', through='LikedPost',
                                   through_fields=('post', 'user'), verbose_name='喜欢文章用户')

    def is_liked_by(self, user):
        '''判断用户 user 是否已经收藏过该文章'''
        return user in self.likers.all()

    def liked_by(self, user):
        '''收藏'''
        if not self.is_liked_by(user):
            LikedPost.objects.create(post=self,user=user)
            # self.likers.append(user)

    def unliked_by(self, user):
        '''取消收藏'''
        if self.is_liked_by(user):
            LikedPost.objects.get(post=self,user=user).delete()
            # self.likers.remove(user)

    class Meta:
        db_table = 'tb_posts'
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-timestamp']




class Comment(models.Model):


    body = models.CharField(max_length=255,verbose_name='评论内容')
    timestamp = models.DateTimeField(db_index=True,auto_now_add=True)
    mark_read = models.BooleanField( default=False)  # 文章作者会收到评论提醒，可以标为已读
    disabled = models.BooleanField( default=False)  # 屏蔽显示
    # 外键，评论作者的 id
    author =models.ForeignKey(to='users.User', related_name="comments",to_field="id",on_delete=models.CASCADE)

    # 外键，评论所属文章的 id
    post=models.ForeignKey(to='Post',related_name='post',on_delete=models.CASCADE)
    # 自引用的多级评论实现
    parent = models.ForeignKey("self",related_name='child',
                               null=True, blank=True,on_delete=models.CASCADE)  # blank=True 在django admin里面可以不填

    liked = models.ManyToManyField('users.User',  through='Likedship',
        through_fields=('comment', 'user'), verbose_name='点赞用户')



    class Meta:
        db_table = 'posts_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        # ordering = ['timestamp']



    def __repr__(self):
        return '<Comment {}>'.format(self.body)

    def get_descendants(self):
        '''递归获取一级评论的所有子孙'''
        data = set()


        def descendants(comment):

            if comment.child: # child 是反向引用

                data.update(comment.child.all().select_related('author','parent','post')) #　update　一次添加多项

                for c in comment.child.all().select_related('author','parent','post'):
                    descendants(c)
        descendants(self)

        return data

    def get_ancestors(self):
        '''获取评论的所有祖先'''
        data = []

        def ancestors(comment):
            if comment.parent:
                data.append(comment.parent)

                ancestors(comment.parent)

        ancestors(self)
        return data

    def switch_like(self, user):
        """点赞或取消赞"""

        # # 如果用户已经赞过，则取消赞
        if user in self.liked.all():
            Likedship.objects.get(user=user,comment=Comment.objects.get(pk=self.pk)).delete()
            # self.liked.remove(user)

        else:
             Likedship.objects.create(user=user,comment=Comment.objects.get(pk=self.pk))




    def count_likers(self):
        """点赞数"""
        return self.liked.count()

    def get_likers(self):
        """获取所有点赞用户"""
        return self.liked.all()


class Likedship(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    timestamp  = models.DateTimeField(auto_now_add=True)




# 喜欢文章
class LikedPost(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)


