import json
from projet3.decorators import ajax_required
from django.views.decorators.csrf import requires_csrf_token
from shop.models import  Produit
from post.models import Post
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404 , redirect, HttpResponseRedirect
from .models import Reaction
from notification.models import Notification
from django.views import generic

from django.http import HttpResponse, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required


@login_required
@ajax_required
def react(request, pk):

  data = {}
  product = Produit.objects.get(pk=pk)
  reaction = request.GET.get('reaction')
 
  has_reacted = Reaction.objects.filter(user=request.user, produit=product).count() == 1
  reaction_choices = Reaction.get_choices()

  

  if has_reacted:
    reaction_obj = request.user.reaction_set.get(produit=product)
    if reaction in reaction_choices :
      if reaction_obj.type != reaction :
        reaction_obj.type = reaction
        reaction_obj.save()
        print(reaction)
        Notification.send(from_user=request.user, to_user=product.boutique.user, product=product, type=reaction)

      else :
        reaction_obj.delete()

      data['reaction'] = reaction
  

    elif not reaction:
      reaction_obj.delete()
      data['reaction'] = ''

  elif reaction in  reaction_choices:
    Reaction.objects.create(user=request.user, produit=product, type=reaction)
    print(reaction)
    Notification.send(from_user=request.user, to_user=product.boutique.user, product=product, type=reaction)
    data['reaction'] = reaction;

  data['count'] = product.reaction_set.count()
  data['count1'] = Reaction.objects.filter(produit=product,type='normal').count()
  print(data['count1'])
  data['count2'] = Reaction.objects.filter(produit=product,type='love').count()
  
  data['count3'] = Reaction.objects.filter(produit=product,type='wish').count()
  data['count4'] = Reaction.objects.filter(produit=product,type='smile').count()
  return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
@ajax_required
def reactPost(request, post_id):

  data = {}
  post = Post.objects.get(pk=post_id)
  reaction = request.GET.get('reaction')
 
  has_reacted = Reaction.objects.filter(user=request.user, post=post).count() == 1
  reaction_choices = Reaction.get_choices()

  

  if has_reacted:
    reaction_obj = request.user.reaction_set.get(post=post)
    if reaction in reaction_choices :
      if reaction_obj.type != reaction :
        reaction_obj.type = reaction
        reaction_obj.save()
        print(reaction)
        Notification.send(from_user=request.user, to_user=post.user, post=post, type=reaction)

      else :
        reaction_obj.delete()

      data['reaction'] = reaction
  

    elif not reaction:
      reaction_obj.delete()
      data['reaction'] = ''

  elif reaction in  reaction_choices:
    Reaction.objects.create(user=request.user, post=post, type=reaction)
    print(reaction)
    Notification.send(from_user=request.user, to_user=post.user, post=post, type=reaction)
    data['reaction'] = reaction;

  data['count'] = post.reaction_set.count()
  data['count1'] = Reaction.objects.filter(post=post,type='like').count()
  print(data['count1'])
  data['count2'] = Reaction.objects.filter(post=post,type='dislike').count()
  
  
  return HttpResponse(json.dumps(data), content_type='application/json')
