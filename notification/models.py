from __future__ import unicode_literals

from django.db import models

import json

from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Count

from django.contrib.auth.models import User

from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from shop.models import Produit
from post.models import Post

# Create your models here.


class Notification(models.Model):
    NORMAL = 'normal'
    SMILE = 'smile'
    LOVE = 'love'
    WISH = 'wish'
    LIKE = 'like'
    DISLIKE = 'dislike'
    COMMENT = 'comment'
    

    NOTIFICATION_TYPES = (
        (NORMAL, 'normal'),
        (SMILE, 'smile'),
        (LOVE, 'love'),
        (WISH, 'wish'),
        (LIKE, 'like'),
        (DISLIKE, 'dislike'),

        (COMMENT, 'comment'),
        #(ALSO_COMMENTED, 'Also Commented'),
    )


    _NORMAL_TEMPLATE = '<a href="/settings/{0}/">{1}</a> has reacted normal to your product: <a href="/discover/produitDetail/{2}/">{3}</a>'  # noqa: E501
    _SMILE_TEMPLATE = '<a href="/settings/{0}/">{1}</a> has reacted with smile to your product: <a href="/discover/produitDetail/{2}/">{3}</a>'  # noqa: E501
    _LOVE_TEMPLATE = '<a href="/settings/{0}/">{1}</a> loves your product: <a href="/discover/produitDetail/{2}/">{3}</a>'  # noqa: E501
    _WISH_TEMPLATE = '<a href="/settings/{0}/">{1}</a> wishes your product: <a href="/discover/produitDetail/{2}/">{3}</a>'  # noqa: E501
    _LIKE_TEMPLATE = '<a href="settings/{0}/">{1}</a> liked your post with category: <a href="/post/postDetail/{2}/">{3}</a>'  # noqa: E501
    _DISLIKE_TEMPLATE = '<a href="settings/{0}/">{1}</a> Disliked your post with category: <a href="/post/postDetail/{2}/">{3}</a>'  # noqa: E501
    _COMMENT_TEMPLATE = '<a href="settings/{0}/">{1}</a> commented your post: <a href="/post/postDetail/{2}/">{3}</a>'  # noqa: E501
    # _ALSO_COMMENTED_TEMPLATE = '<a href="settings/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    product = models.ForeignKey(Produit, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
   # feed = models.ForeignKey('feeds.Feed', null=True, blank=True)
    type = models.CharField(max_length=255, choices=NOTIFICATION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.type == self.NORMAL:
            return self._NORMAL_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.product.pk,
                escape(self.get_summary(self.product.title))
                )
        elif self.type == self.SMILE:
            return self._SMILE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.product.pk,
                escape(self.get_summary(self.product.title))
                )
        elif self.type == self.LOVE:
            return self._LOVE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.product.pk,
                escape(self.get_summary(self.product.title))
                )
        elif self.type == self.WISH:
            return self._WISH_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.product.pk,
                escape(self.get_summary(self.product.title))
                )
        elif self.type == self.LIKE:
            return self._LIKE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.post.pk,
                escape(self.get_summary(self.post.categorie.name))
                )
        elif self.type == self.DISLIKE:
            return self._DISLIKE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.post.pk,
                escape(self.get_summary(self.post.categorie.name))
                )    
        elif self.type == self.COMMENT:
            return self._COMMENT_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.post.pk,
                escape(self.get_summary(self.post.categorie.name))
                )
        # elif self.type == self.ALSO_COMMENTED:
        #     return self._ALSO_COMMENTED_TEMPLATE.format(
        #         escape(self.from_user.username),
        #         escape(self.from_user.profile.get_screen_name()),
        #         self.feed.pk,
        #         escape(self.get_summary(self.feed.post))
        #         )    


        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value
    

    def send(from_user, to_user, type, product=None, post=None):
        if (product and not post) or (post and not product):
            notification = Notification(from_user=from_user,
                                        to_user=to_user,
                                        product=product,
                                        post=post,
                                        type=type).save()
            return notification
        return None