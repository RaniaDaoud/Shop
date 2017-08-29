from django.db import models
from django.contrib.auth.models import Permission, User
import datetime
#from shop.models import Produit


class Wishlist(models.Model):
    product = models.ManyToManyField('shop.Produit')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name