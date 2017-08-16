from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from notification import views as activities_views


urlpatterns = [
    
	url(r'^notifications/$', activities_views.notifications, name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications, name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications, name='check_notifications'),
]	