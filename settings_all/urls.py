from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from settings_all import views as core_views




urlpatterns = [

    url(r'^settings/$', core_views.settings, name='settings'),
	url(r'^settings/picture/$', core_views.picture, name='picture'),
	url(r'^settings/upload_picture/$', core_views.upload_picture,name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,name='save_uploaded_picture'),
	url(r'^settings/password/$', core_views.password, name='password'),
	
    url(r'^settings/(?P<username>[^/]+)/$', core_views.profileR, name='profile'),
    
    
    
]