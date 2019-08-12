
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token




urlpatterns = [


    url('^users/$', views.UserViewSet.as_view()),
    url('^users/(?P<pk>\d+)/$', views.UserViewSetView.as_view()),
    url('^follow/(?P<pk>\d+)/$', views.FollowView.as_view()),
    url('^unfollow/(?P<pk>\d+)/$', views.UnFollowView.as_view()),

    #  资源里的评论
    url('^users/(?P<pk>\d+)/comments/$', views.UserCommentsVIew.as_view()),
    #

    url('^users/(?P<pk>\d+)/followeds/$', views.FollowedView.as_view()),
    # 通知里的 粉丝
    url('^users/(?P<pk>\d+)/followers/$', views.FollowerView.as_view()),
    url('^users/(?P<pk>\d+)/posts/$', views.MyDynamicVIew.as_view()),
    url('^users/(?P<pk>\d+)/followeds-posts/$', views.FollowedsPostsVIew.as_view()),

    # 通知列表里面的评论
    url('^users/(?P<pk>\d+)/recived-comments/$', views.UserReceivedCommentsVIew.as_view()),

    # 通知列表里面的点赞
    url('^users/(?P<pk>\d+)/recived-comments-likes/$', views.UserReceivedLikesVIew.as_view()),


    # 我的资源里的私信列表，
    url('^users/(?P<pk>\d+)/messages-recipients/$', views.GetUserListMessagesRecipients.as_view()),

    # 未读私信通知
    url('^users/(?P<pk>\d+)/messages-senders/$', views.GetUserMessagesSenders.as_view()),
    url('^users/(?P<pk>\d+)/history-messages/$', views.GetUserHistoryMessages.as_view()),
    # url('^users/(?P<pk>\d+)/history-messages/$', views.GetUserListMessagesRecipients.as_view()),

    # 黑名单
    url('^block/(?P<pk>\d+)/$', views.BlockView.as_view()),
    url('^unblock/(?P<pk>\d+)/$', views.UnBlockView.as_view()),


    url('^users/(?P<pk>\d+)/recived-posts-likes/$', views.UserReceivedPostsLikesVIew.as_view()),
    url('^users/(?P<pk>\d+)/liked-posts/$', views.UserLikesPostsVIew.as_view()),

    url('^tokens/$', obtain_jwt_token)

]
