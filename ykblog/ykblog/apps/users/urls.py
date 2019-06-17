
from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^users/$', views.UserViewSet.as_view({'post': 'create'})), #
    # url(r'^users/$', views.UserViewSet.as_view({'get': 'list'})), #
    # # url(r'^books/latest/$', views.BookInfoViewSet.as_view({'get': 'latest'})),
    # url(r'^users/(?P<pk>\d+)/$', views.UserViewSet.as_view({'get': 'retrieve'}),name='user-retrieve'),
    # url(r'^users/(?P<pk>\d+)/$', views.UserViewSet.as_view({'put': 'update'})),
    # url(r'^books/$', views.BookInfoViewSet.as_view({'get': 'list'})),
    # url(r'^books/latest/$', views.BookInfoViewSet.as_view({'get': 'latest'})),
    # url(r'^books/(?P<pk>\d+)/$', views.BookInfoViewSet.as_view({'get': 'retrieve'})),
    # url(r'^books/(?P<pk>\d+)/read/$', views.BookInfoViewSet.as_view({'put': 'read'})),

    url('users/$', views.UserViewSet.as_view()),
    url('users/(?P<pk>\d+)/$', views.UserViewSetView.as_view())
]
"""
HTTP方法	资源URL	说明
GET	/api/users	返回所有用户的集合
POST	/api/users	注册一个新用户
GET	/api/users/<id>	返回一个用户
PUT	/api/users/<id>	修改一个用户
DELETE	/api/users/<id>	删除一个用户
"""