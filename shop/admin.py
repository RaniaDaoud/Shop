from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Boutique, Produit
from authentication.models import  Utilisateur
from messenger.models import Message
from reaction.models import Reaction
from notification.models import Notification
from post.models import *
# Register your models here.
admin.site.register(Boutique)
admin.site.register(Produit)
admin.site.register(Message)
admin.site.register(Utilisateur)
admin.site.register(Reaction)
admin.site.register(Notification)
admin.site.register(Categorie)
admin.site.register(Post)
admin.site.register(Comment)




