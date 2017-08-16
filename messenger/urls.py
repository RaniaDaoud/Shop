from django.conf.urls import url

from messenger import views

urlpatterns = [
    url(r'^recherche/$', views.search, name='searchP'),
    url(r'^sendIMG/$', views.send_IMG, name='send_IMG'),
    url(r'^new/$', views.new, name='new_message'),
    url(r'^new1/$', views.newM, name='new_message1'),
    url(r'^send/$', views.send, name='send_message'),
    url(r'^sendMes/$', views.sendMes, name='send_messageMes'),
    #url(r'^sendP/$', views.sendP, name='send_messageP'),
    url(r'^delete/(?P<message_id>[0-9]+)/$', views.delete, name='delete_message'),
    url(r'^users/$', views.users, name='users_message'),
    url(r'^check/$', views.check, name='check_message'),
    url(r'^(?P<username>[^/]+)/$', views.messages, name='messages'),
    url(r'^$', views.inbox, name='inbox'),
]
