from django.conf.urls import url
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('search', views.PostSearchViewSet, base_name='posts_search')

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

    url('^posts/browseList/$', views.artViewList.as_view()),
    url('^posts/classList/$', views.CategoryListView.as_view()),
    url('^category/$', views.CategoryPostView.as_view()),

    url('^time/$', views.TimePostView.as_view()),


    path('upload_file/', views.upload_file, name='upload_file'),
]


urlpatterns += router.urls