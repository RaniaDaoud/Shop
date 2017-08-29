from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from settings_all import views as core_views
from reaction import views as reaction_views






urlpatterns = [
    url(r'^api/shop/', include("shop.api.urls", namespace='shop-api')),
    url(r'^api/notification/', include("notification.api.urls", namespace='notification-api')),
    url(r'^api/msg/', include("messenger.api.urls", namespace='messenger-api')),
    url(r'^api/reaction/', include("reaction.api.urls", namespace='reaction-api')),

    url(r'^album/', include('album.urls')),
     url(r'^whishlist/', include('wish_list.urls')),
    
    

    url(r'^', include('post.urls')),
    url(r'^reactPost/(?P<post_id>\d+)/$', reaction_views.reactPost, name='reactPost'),
   
   
    #url(r'^feeds/', include('feeds.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('authentication.urls')), 
    url(r'^', include('notification.urls')),
    
    
    
    url(r'^boutique/', include('shop.urls')),
    url(r'^discover/', include('discover.urls')),
    url(r'^', include('settings_all.urls')),

	url(r'^messages/', include('messenger.urls')),
	url(r'^react/(?P<pk>\d+)/$', reaction_views.react, name='react'),
    

    
	
	
]	

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)