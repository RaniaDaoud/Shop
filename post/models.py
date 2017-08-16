from django.db import models
from django.contrib.auth.models import Permission, User
import datetime

now = datetime.datetime.now()
def group_based_upload(instance, filename):
    return "post/categorie/{}".format(str(now)+' -- '+filename)
  


class Categorie(models.Model) :
    name = models.CharField(max_length=250,verbose_name="Nom du categorie")
    user = models.ForeignKey(User, default=1)
    logo = models.ImageField(upload_to=group_based_upload,null=True, blank=True)
    
    def __str__(self):
        return self.logo.url


def group_based_uploadPost(instance, filename):
    return "post/attach/{}".format(str(now)+' -- '+filename)  

class Post(models.Model) :
    post = models.TextField(max_length=250)
    user = models.ForeignKey(User, default=1)
    image = models.ImageField(upload_to= group_based_uploadPost,null=True, blank=True)
    categorie = models.ForeignKey(Categorie, blank=False,default='1')
    date = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ('-date',)
    def __str__(self):
        return self.post    
    
    
    @staticmethod
    def send_post(user, post, categorie, image=None):
        #message = message[:1000]
        
        current_user_post = Post(user=user,
                                 post=post,
                                 categorie=categorie,
                                image=image,
                                       
                                       )
        current_user_post.save()
        

        return current_user_post

    def get_reaction(self):
        return self.reaction_set.count()

    def get_like(self):
        return self.reaction_set.filter(type='like').count()

    def get_dislike(self):
        return self.reaction_set.filter(type='dislike').count()
   

 


class Comment (models.Model) :
    text = models.TextField(max_length=250)
    user = models.ForeignKey(User, default=1)
    post = models.ForeignKey(Post, default=1, related_name='comments')
    date = models.DateTimeField(auto_now_add=True,null=True) 
    
    class Meta:
        ordering = ('-date',)
    def __str__(self):
        return self.text   
        