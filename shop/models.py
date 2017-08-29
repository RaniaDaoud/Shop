from django.db import models
from django.contrib.auth.models import Permission, User
import datetime
from taggit.managers import TaggableManager
#from wish_list.models import Wishlist


now = datetime.datetime.now()
def group_based_upload(instance, filename):
    return "image/media/{}/{}/{}".format(instance.user,instance.name,str(now)+' -- '+filename)

class Boutique(models.Model):
    name = models.CharField(max_length=250,verbose_name="Name")
    user = models.ForeignKey(User, default=1)
    logo = models.ImageField(upload_to=group_based_upload,null=True,verbose_name="Shop Logo")
    
    visitors = models.ManyToManyField(User, related_name="visiteurs")
    
    date = models.DateTimeField(auto_now_add=True,null=True)    
    

    def __str__(self):
        return self.name


#+'--'+str(now)
def group_based_upload_to(instance, filename):
    return "image/media/{}/{}/{}/{}".format(instance.boutique.user,instance.boutique.name,instance.title ,str(now)+' -- '+filename)

class Produit(models.Model):
    
    prix = models.IntegerField(null=True, verbose_name="Price")
    title = models.CharField(max_length=250,verbose_name="Name")
    descreption = models.CharField(max_length=250, verbose_name="Description")
    logo = models.ImageField(upload_to=group_based_upload_to,null=True,verbose_name="Principal photo")
    logo1 = models.ImageField(upload_to=group_based_upload_to,default=None, blank=True)
    logo2 = models.ImageField(upload_to=group_based_upload_to,null=True, blank=True)
    logo3 = models.ImageField(upload_to=group_based_upload_to,null=True, blank=True)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE , verbose_name="Shop")
    is_favorite = models.BooleanField(default=False)
    choix = (('All products','All products'),('Jewelry','Jewelry'),('Home & Furnishings','Home & Furnishings'),('Clothes','Clothes'),('Art & collections','Art & collections'),('Accessoires','Accessoires'))
    categorie = models.CharField(max_length=250,choices=choix,default=None, verbose_name="Category")
    typeProduit = models.CharField(max_length=250,choices=(('Handmade','Handmade'),('Vintage','Vintage')),default=None, verbose_name="Type")
    created = models.DateTimeField(auto_now_add=True, null=True)
   # updated = models.DateTimeField(auto_now_add=False, auto_now=True , default=None)
    quantite = models.IntegerField(default=None, verbose_name="Quantity")
    Genre = models.CharField(max_length=250,choices=(('Men & women','Men & women'),('Men','Men'),('Women','Women')),null=True, verbose_name="Gender")
    options = (('standard','standard'),('baby','baby'),('child','child'),('young','young'),('adult','adult')) 
    pour = models.CharField(max_length=250,choices=options,null=True, verbose_name="For")
    
    

    tags = TaggableManager()

    def __str__(self):  # __unicode__ on Python 2
        return self.title

    def get_reaction(self):
        return self.reaction_set.count()

    def get_normal(self):
        return self.reaction_set.filter(type='normal').count()

    def get_smile(self):
        return self.reaction_set.filter(type='smile').count()

    def get_wish(self):
        return self.reaction_set.filter(type='wish').count()

    def get_love(self):
        return self.reaction_set.filter(type='love').count()

    class Meta:
        ordering = ('title',)

    def get_absolute_url(self):
        return self.logo.url
