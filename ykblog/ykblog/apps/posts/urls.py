
from django.conf.urls import url
from . import views



urlpatterns = [


    url('posts/$', views.PostViewSet.as_view()),
    url('posts/(?P<pk>\d+)/$', views.PostViewSetView.as_view()),

]
