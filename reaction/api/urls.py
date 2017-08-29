from django.conf.urls import url

from . views import (ReactionCreateAPIView, )


urlpatterns =[
    
    url(r'^create/(?P<prod_id>\d+)/$', ReactionCreateAPIView.as_view(), name='create'),

]