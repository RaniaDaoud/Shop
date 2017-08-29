from django.conf.urls import url
from .  import views

urlpatterns=[

    #url(r'^(?P<user_id>[0-9]+)/$', views.post_update, name='wishlist'),
    url(r'^(?P<user_id>[0-9]+)/wishlist/$', views.wishlist, name='wishlist'),
    url(r'^(?P<user_id>[0-9]+)/wishlist/(?P<wishlist>[^/]+)/$', views.wishlist, name='wishlist'),
    #url(r'^(?P<shop_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_wishlist/$', views.create_wishlist, name='create_wishlist'),
    url(r'^delete_wishlist/(?P<wl_id>[0-9]+)/$', views.delete_wishlist, name='delete_wishlist'),
    url(r'^add_to_wishlist/(?P<prod_id>[0-9]+)/$', views.add_to_wishlist, name='add_to_wishlist'),
    url(r'^(?P<wish_id>[0-9]+)/(?P<prod_id>[0-9]+)$', views.delete_wish_view, name='deletewish'),


]