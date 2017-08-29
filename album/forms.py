from django.forms import ModelForm

from album.models import Photo


class PhotoForm(ModelForm):
  class Meta:
    model = Photo
    fields = ['image']