from django.db import models

# Create your models here.

from authentication.models import Utilisateur
import datetime

now = datetime.datetime.now()
def get_photo_link(instance, filename):
    return "image/media/album/{}/{}".format(instance.album.utilisateur.user,str(now)+' -- '+filename)


class Album(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, null=True)

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=get_photo_link)
    date = models.DateTimeField(auto_now_add=True)