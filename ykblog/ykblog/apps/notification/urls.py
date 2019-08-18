from django.conf.urls import url

from . import views


urlpatterns = [

    url('^users/(?P<pk>\d+)/notifications/', views.UserNotificationView.as_view()),
    url('^notifications/(?P<pk>\d+)/$', views.notificationView.as_view()),


]
