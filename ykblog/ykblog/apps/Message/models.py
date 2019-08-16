from django.db import models
from django.conf import settings
# Create your models here.
class Message(models.Model):


    body = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True,db_index=True)
    # 用户发送的私信
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='messages_sent',on_delete=models.CASCADE)
    # 用户接收的私信

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='messages_received',on_delete=models.CASCADE)

    def __str__(self):
        return '<Message {}>'.format(self.pk)

    class Meta:
        db_table = 'messages'
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        # ordering = ['-timestamp']


class ShowLikeData(models.Model):

    num = models.IntegerField(default=0)
    class Meta:
        db_table = 'sitelike'
        verbose_name = '站点喜欢'
        verbose_name_plural = verbose_name