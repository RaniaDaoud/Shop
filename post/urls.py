from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



from post import views as post_views





urlpatterns = [
    url(r'^searchPost/$', post_views.searchPost, name='searchPost'),
    #url(r'^post/postDetail/comment/$', post_views.post_comment_view, name='post_comment'),
    url(r'^post/postDetail/(?P<post_id>\d+)/comment/$', post_views.post_comment_view, name='post_comment'),
    url(r'^post/postDetail/(?P<post_id>\d+)/$', post_views.post_detail_view, name='DetailPost'),
    #url(r'^post/postDetail/(?P<pk>[0-9]+)/$', post_views.detailPost.as_view(), name='DetailPost'),    
    url(r'^post/$', post_views.posts, name='posts'),
    url(r'^post/one/$', post_views.post, name='post'),
    url(r'^post/all/$', post_views.post_posts, name='postALL'),



    ]