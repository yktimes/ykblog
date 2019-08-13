
from django.conf.urls import url
from . import views



urlpatterns = [

    #
    url('^messages/$', views.MessageView.as_view()),
url('^messages/(?P<pk>\d+)/$', views.MessagesViewSetView.as_view()),
url('^send-messages/$', views.MessagesAllView.as_view()),
]
