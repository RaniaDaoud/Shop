from django.conf.urls import url
from . import views
app_name = 'boutique'
urlpatterns=[

    
    url(r'^$', views.index, name='index'),
   
    

    
    url(r'^(?P<produit_id>[0-9]+)/$', views.post_update, name='post_update'),
    url(r'^(?P<produit_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^create_boutique/$', views.create_boutique, name='create_boutique'),
    url(r'^produit/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='DetailView1'),
    url(r'^shop/(?P<Boutique_id>[0-9]+)/$', views.post_updateBoutique, name='post_updateB'),
    url(r'^user/(?P<Boutique_id>[0-9]+)/$', views.post_updateUser, name='post_updateU'),

   

 
    url(r'^(?P<boutique_id>[0-9]+)/create_produit/$', views.create_produit, name='create_produit'),
    url(r'^(?P<boutique_id>[0-9]+)/delete_produit/(?P<produit_id>[0-9]+)/$', views.delete_produit, name='delete_produit'),
    url(r'^dupliquer/(?P<produit_id>[0-9]+)/$', views.dupliquer, name='dupliquer'),
    

  

    url(r'^detail/(?P<boutique_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<boutique_id>[0-9]+)/delete_boutique/$', views.delete_boutique, name='delete_boutique'),
   
   


]

