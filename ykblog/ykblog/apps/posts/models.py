from django.db import models
from django.conf import settings
from users.models import User
# Create your models here.

class Post(models.Model):


    title = models.CharField(max_length=255,verbose_name='标题')
    summary = models.CharField(max_length=255,verbose_name='总结概括')

    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    views =models.IntegerField(default=0)
    author = models.ForeignKey(User,related_name='posts')
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
    author =models.ForeignKey(to='users.User', related_name="author",to_field="id")

    # 外键，评论所属文章的 id
    post=models.ForeignKey(to='Post',related_name='post')
    # 自引用的多级评论实现
    parent = models.ForeignKey("self",related_name='child',
                               null=True, blank=True,on_delete=models.CASCADE)  # blank=True 在django admin里面可以不填

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