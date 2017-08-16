from django.db import models
from django.contrib.auth.models import Permission, User
import datetime

now = datetime.datetime.now()
def group_based_upload(instance, filename):
    return "image/media/{}/{}/{}".format(instance.user,instance.name,str(now)+' -- '+filename)

class Boutique(models.Model):
    name = models.CharField(max_length=250,verbose_name="Nom du Boutique")
    user = models.ForeignKey(User, default=1)
    logo = models.ImageField(upload_to=group_based_upload,null=True, blank=True,verbose_name="Logo_Boutique")
    
    
    
    date = models.DateTimeField(auto_now_add=True,null=True)    
    

    def __str__(self):
        return self.name


#+'--'+str(now)
def group_based_upload_to(instance, filename):
    return "image/media/{}/{}/{}/{}".format(instance.boutique.user,instance.boutique.name,instance.title ,str(now)+' -- '+filename)

class Produit(models.Model):
    prix = models.IntegerField()
    title = models.CharField(max_length=250)
    descreption = models.CharField(max_length=250)
    logo = models.ImageField(upload_to=group_based_upload_to,null=True)
    logo1 = models.ImageField(upload_to=group_based_upload_to,default=None, blank=True)
    logo2 = models.ImageField(upload_to=group_based_upload_to,null=True, blank=True)
    logo3 = models.ImageField(upload_to=group_based_upload_to,null=True, blank=True)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    choix = (('Tous les produits','Tous les produits'),('Bijoux','Bijoux'),('Maison et ameublement','Maison et ameublement'),('Vetement','Vetement'),('Art et collections','Art et collections'),('Accessoires','Accessoires'))
    categorie = models.CharField(max_length=250,choices=choix,default=None)
    typeProduit = models.CharField(max_length=250,choices=(('Faits à main','Faits à main'),('Vintage','Vintage')),default=None)
    created = models.DateTimeField(auto_now_add=True, null=True)
   # updated = models.DateTimeField(auto_now_add=False, auto_now=True , default=None)
    quantite = models.IntegerField(default=None)


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


