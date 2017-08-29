from django.db import models
from django.contrib.auth.models import Permission, User
from shop.models import Produit
from post.models import Post
# Create your models here.

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE ,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE ,null= True)  
    choix = (('normal', 'normal'), ('smile', 'smile'), ('love', 'love'), ('wish', 'wish'),('like','like'),('dislike','dislike'))
    type = models.CharField(max_length=255, blank=True, null=True, choices=choix)
    date = models.DateTimeField(auto_now_add = True)

    class Meta: 
     	unique_together =(('user','produit','post'),)

    @staticmethod
    def get_choices():
        return [choice[1] for choice in Reaction._meta.get_field('type').choices]



class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
        )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    @staticmethod
    def monthly_activity(user):
        """Static method to retrieve monthly statistical information about the
        user activity.
        @requires:  user - Instance from the User Django model.
        @returns:   Two JSON arrays, the first one is dates which contains all
                    the dates with activity records, and the second one is
                    datapoints containing the sum of all the activity than had
                    place in every single month.

        Both arrays keep the same order, so there is no need to order them.
        """
        # months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        # "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        query = Activity.objects.filter(user=user).annotate(
            month=TruncMonth('date')).values('month').annotate(
                c=Count('id')).values('month', 'c')
        dates, datapoints = zip(
            *[[a['c'], str(a['month'].date())] for a in query])
        return json.dumps(dates), json.dumps(datapoints)

    @staticmethod
    def daily_activity(user):
        """Static method to retrieve daily statistical information about the
        user activity.
        @requires:  user - Instance from the User Django model.
        @returns:   Two JSON arrays, the first one is dates which contains all
                    the dates with activity records, and the second one is
                    datapoints containing the sum of all the activity than had
                    place in every single day.

        Both arrays keep the same order, so there is no need to order them.
        """
        query = Activity.objects.filter(user=user).annotate(day=TruncDay(
            'date')).values('day').annotate(c=Count('id')).values('day', 'c')
        dates, datapoints = zip(
            *[[a['c'], str(a['day'].date())] for a in query])
        return json.dumps(dates), json.dumps(datapoints)

    def __str__(self):
        return self.activity_type        