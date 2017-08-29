from django.shortcuts import render, redirect, get_object_or_404
from wish_list.models import Wishlist
from shop.models import Produit
from django.contrib.auth.models import Permission, User
import json
from django.http import JsonResponse
from projet3.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.


def wishlist(request,user_id, wishlist=''):
    user = User.objects.get(id=user_id)
    wishlists = Wishlist.objects.filter(user=user)
    #for wish in wishlists :
        #print(wish.product_set.all)
    prodsAll = Produit.objects.all()
    print(prodsAll)
    prods=None
    wishlist11= None
    name = None
    if wishlists.first():
        prods = Produit.objects.filter(wishlist=wishlists.first())
        if wishlists :
            wishlist11 = wishlists.first().id
            name= wishlists.first().name


    #curr_time = timezone.now() + timedelta(hours=1)
    counter = []
    #interacts = None
    #if request.user.is_authenticated():
    #    interacts = Interaction.objects.filter(user=request.user)

    for col in wishlists:
        counter.append((col, prodsAll.filter(wishlist=col).count()))

    if not wishlist == '':
        prods = Produit.objects.filter(wishlist__name=wishlist)
        if wishlists :
            wishlist11 = Wishlist.objects.filter(name=wishlist).first().id
            name = Wishlist.objects.filter(name=wishlist).first().name
        
      
    return render(request, 'wishlist/wishlist.html', { 'prods': prods,'counter':counter, 'wishlist':wishlist11, 'name':name,'user':user})

def create_wishlist(request):
    name = request.POST.get('wishlist_name')
    #curr_time = timezone.now() + timedelta(hours=1)
    Wishlist.objects.create(user=request.user,name=name)
    wishlists = Wishlist.objects.filter(user=request.user)
    prods = None
    if wishlists.first():
        prods = Produit.objects.filter(wishlist=wishlists.first())
        
        wishlist11 = wishlists.first().id
        name= wishlists.first().name

    counter = []
    #interacts = None
    #if request.user.is_authenticated():
    #    interacts = Interaction.objects.filter(user=request.user)

    for col in wishlists:
        counter.append((col, prods.filter(wishlist=col).count()))
    return render(request, 'wishlist/wishlist.html', {'prods':prods,'counter':counter,'wishlist':wishlist11, 'name':name})



def delete_wishlist(request,wl_id):
    #curr_time = timezone.now() + timedelta(hours=1)
    wishlist = Wishlist.objects.get(id =wl_id)
    wishlist.delete()

    wishlists = Wishlist.objects.filter(user=request.user)
    prods = None
    if wishlists.first():
        prods = Produit.objects.filter(wishlist=wishlists.first())
        
        wishlist11 = wishlists.first().id
        name= wishlists.first().name
    counter = []
    #interacts = None
    #if request.user.is_authenticated():
    #    interacts = Interaction.objects.filter(user=request.user)

    for col in wishlists:
        counter.append((col, prods.filter(wishlist=col).count()))
    return render(request, 'wishlist/wishlist.html', {'prods':prods,'counter':counter,'wishlist':wishlist11, 'name':name})


#@ajax_required
def add_to_wishlist(request, prod_id):
    prod = Produit.objects.get(id = prod_id)
    wishlists = Wishlist.objects.filter(user=request.user)
    #nom = request.POST.get('name')
    #print(nom)
    #print(wishlists)
    for w in wishlists:
        name = request.POST.get(w.name)
        #print(prod.name)
        #print(w.name)
        print(name)
        if name:
            w.product.add(prod)
            w.save()
    #return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    return redirect('/discover/produit/')
        #return HttpResponse(json.dumps({'success': True, 'checked': True}), content_type='application/json')
    #return HttpResponse()


@login_required
@ajax_required
def delete_wish_view(request, wish_id, prod_id):
    print('enter')
    if request.method == 'POST':
        wishlist = get_object_or_404(Wishlist, pk=wish_id)
        #collection = request.user.wishlist.collections.get(pk=wish_id)
        produit = Produit.objects.get(pk=prod_id)
        #wishlist.product.remove(produit)
        print(produit)
        if produit in wishlist.product.all():
            wishlist.product.remove(produit)
        return HttpResponse(json.dumps({'success': True, 'checked': False}), content_type='application/json')
    return HttpResponse()    
        #print(a)
        #produit = Produit.objects.get(pk=prod_id)
        #produit.delete() 
        #request.user.utilisateur.album.photos.get(pk=pk).delete()
    #return render(request, 'album/photo.html', {'photos': photos})
    #    return redirect('/discover/produit/')   
   # else :
    #    print('test')
    #    return redirect('/discover/produit/')  
    #return redirect('/discover/produit/')   
 
   
    #return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    