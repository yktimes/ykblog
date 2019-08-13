import xadmin
from .models import Message

class MessageAdmin(object):
    list_display = ['id', 'body','timestamp', 'sender', 'recipient']

    show_detail_fields = ['id']

xadmin.site.register(Message, MessageAdmin)