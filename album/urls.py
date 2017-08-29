from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^album/(?P<user_id>\d+)$', views.album, name='album1'),
    url(r'^$', views.create_album, name='album'),
    url(r'^new/$', views.new_photo_view, name='new_photo'),
    url(r'^delete/(?P<pk>\d+)$', views.delete_photo_view, name='delete_photo'),

]