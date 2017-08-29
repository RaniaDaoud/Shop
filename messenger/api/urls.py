from django.conf.urls import url

from . views import (MsgListAPI,
MsgCreateAPIView, )


urlpatterns =[
    url(r'^get/(?P<username>[-\w]+)/$',MsgListAPI.as_view(),name='list_Msg'),
    url(r'^create/(?P<to_user>[-\w]+)/$', MsgCreateAPIView.as_view(), name='create'),

]