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


