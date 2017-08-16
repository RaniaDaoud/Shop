from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from authentication import views as bootcamp_auth_views
from settings_all import views as core_views
from reaction import views as reaction_views






urlpatterns = [
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