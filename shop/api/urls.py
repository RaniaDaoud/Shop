from django.conf.urls import url

from . views import (ProductListAPI, 
	DetailListAPI, )


urlpatterns =[
    url(r'^$',ProductListAPI.as_view(),name='list'),
    url(r'^(?P<prod_id>\d+)/$',DetailListAPI.as_view(),name='detail'),

]