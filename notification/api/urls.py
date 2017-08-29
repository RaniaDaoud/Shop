from django.conf.urls import url

from . views import (NotifListAPI, )


urlpatterns =[
    url(r'^(?P<username>[-\w]+)/$',NotifListAPI.as_view(),name='list_Notif')

]