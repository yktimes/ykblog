
from django.conf.urls import url
from . import views



urlpatterns = [

    #
    url('^posts/$', views.PostViewSet.as_view()),
    url('^posts/(?P<pk>\d+)/$', views.PostViewSetView.as_view()),
    url('^posts/(?P<pk>\d+)/comments/$', views.PostCommentView.as_view()),



    url('^comments/$', views.CommentsView.as_view()),
    url('^comments/(?P<pk>\d+)/$', views.CommentsViewSetView.as_view()),

    url('^comments/(?P<pk>\d+)/like/$', views.LikeView.as_view()),

    url('^posts/(?P<pk>\d+)/like/$', views.LikePostView.as_view()),
    url('^posts/(?P<pk>\d+)/unlike/$', views.UnLikePostView.as_view()),


]
