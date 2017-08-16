
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from authentication import views as bootcamp_auth_views




urlpatterns = [

url(r'^signup/$', bootcamp_auth_views.signup, name='signup'),
url(r'^login/$', bootcamp_auth_views.login_user, name='login'),
url(r'^login_userM/$', bootcamp_auth_views.login_userM, name='login_userM'),
url(r'^utilisateur/$', bootcamp_auth_views.utilisateur, name='utilisateur_register'),
url(r'^logout', bootcamp_auth_views.logout_user,  name='logout'),   


]
