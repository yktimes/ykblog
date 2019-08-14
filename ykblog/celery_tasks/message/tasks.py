
import logging

from users.models import User
from Message.models import Message

from celery_tasks.main import app
import sys
logger = logging.getLogger('django')

from .constants import EMAIL


from django.db.models import Q

@app.task(name='send_messages')
def send_messages(*args, **kwargs):
    '''群发私信'''

    try:  # 由于 运行在单独的进程中，当它出现意外错误时，我们需要捕获异常

        # 发送方
        sender = User.objects.get(id=kwargs.get('kwargs').get('user_id'))
        # 接收方
        recipients = User.objects.filter(~Q(id=kwargs.get('kwargs').get('user_id')))


        for i, user in enumerate(recipients):
            message = Message()
            message.body =kwargs.get('kwargs').get('body')
            message.sender = sender
            message.recipient = user
            message.save()
            # 给私信接收者发送新私信通知
            user.add_notification('unread_messages_count', user.new_recived_messages())
            user.save()


        # 群发结束后，由管理员给自己发送一个提示消息

        admin = User.objects.filter(email=EMAIL).first()

        message = Message()
        message.body = '[群发私信]已完成, 内容: \n\n' + kwargs.get('kwargs').get('body')
        message.sender = admin
        message.recipient = admin
        message.save()
        # 给发送方发送新私信通知
        admin.add_notification('unread_messages_count', admin.new_recived_messages())
        admin.save()

    except Exception:
        logger.error('[群发私信]后台任务出错了', exc_info=sys.exc_info())


