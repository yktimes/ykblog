
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token




urlpatterns = [


    url('^users/$', views.UserViewSet.as_view()),
    url('^users/(?P<pk>\d+)/$', views.UserViewSetView.as_view()),
    url('^follow/(?P<pk>\d+)/$', views.FollowView.as_view()),
    url('^unfollow/(?P<pk>\d+)/$', views.UnFollowView.as_view()),


    #
    url('^users/(?P<pk>\d+)/followeds/$', views.FollowedView.as_view()),
    url('^users/(?P<pk>\d+)/followers/$', views.FollowerView.as_view()),
    url('^users/(?P<pk>\d+)/posts/$', views.MyDynamicVIew.as_view()),
    url('^users/(?P<pk>\d+)/followeds-posts/$', views.FollowedsPostsVIew.as_view()),


url('^users/(?P<pk>\d+)/comments/$', views.UserReceivedCommentsVIew.as_view()),

    url('^tokens/$', obtain_jwt_token)

]
