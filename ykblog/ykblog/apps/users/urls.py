
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token




urlpatterns = [


    url('users/$', views.UserViewSet.as_view()),
    url('users/(?P<pk>\d+)/$', views.UserViewSetView.as_view()),

    url('tokens/$', obtain_jwt_token)

]
