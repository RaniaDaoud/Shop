from django.conf.urls import url
from . import views
app_name = 'discover'
urlpatterns=[
    
    url(r'^products/$', views.products, name='products'),
    
    url(r'^liste/(?P<pk>\d+)/$', views.boutique, name='boutique'),     
    url(r'^produitDetail/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='DetailView1'),
    
   
    url(r'^produit/$', views.post_list, name='postlist'),

    url(r'^filtrell/$', views.filter2, name='filter2'),
    url(r'^search/$', views.search, name='search'),
    url(r'^auto/$', views.auto, name='auto'),
 
   


]

