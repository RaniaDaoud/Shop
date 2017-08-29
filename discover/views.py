import json
from projet3.decorators import ajax_required
from django.views.decorators.csrf import requires_csrf_token
from shop.models import Boutique, Produit
from post.models import Post

from shop.forms import BoutiqueForm,  ProduitForm
from authentication.models import Utilisateur
from authentication.forms import  BusinessUserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404 , redirect, HttpResponseRedirect
from django.db.models import Q
from django.views import generic
from messenger.models import Message 
from album.models import Album
from wish_list.models import Wishlist
from django.http import HttpResponse, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required
from messenger.models import Message





IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class DetailView(generic.DetailView):
    model = Produit
   
    template_name = 'discover/detailProduit.html'
    

def post_list(request):
    counter2=[]
    
    list_produit = Produit.objects.filter(is_favorite=True)
    if request.user.is_authenticated():    
        user = request.user
        age = user.profile.age 
        print(age)
        counter2 = Wishlist.objects.filter(user=user)
        
        if age < 3 :
            list_produit = Produit.objects.filter(Q(pour='baby') | Q(pour='standard') | Q(Genre__contains='men') | Q(Genre__contains='women')) 
        elif age > 3 and (age < 14) :
            list_produit = Produit.objects.filter(Q(pour='child') | Q(pour='standard') | Q(Genre__contains='men') | Q(Genre__contains='women'))
        elif age > 14 and (age < 19) :
            list_produit = Produit.objects.filter(Q(pour='young') | Q(pour='standard') | Q(Genre__contains='men') | Q(Genre__contains='women'))
        elif age > 19 :
            list_produit = Produit.objects.filter(Q(pour='adult') | Q(pour='standard') | Q(Genre__contains='men') | Q(Genre__contains='women'))        
        else :
            list_produit = Produit.objects.all()
            print('ok')
        print(list_produit)
    else :    
        list_produit = Produit.objects.filter(is_favorite=True)

    paginator = Paginator(list_produit,8)
    page = request.GET.get('page')
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)

    context={
        'counter2':counter2,
        'page':page, 
        'minx': min( [post['prix'] for post in list_produit.values('prix')] ),
        'maxx': max([post['prix'] for post in list_produit.values('prix')]),
        'produits': produits, 
        'Tous':Produit.objects.filter(is_favorite=True).count(), 
        'Bijoux':list_produit.filter(categorie='Jewelry').count(), 
        'Vetement':list_produit.filter(categorie='Clothes').count(), 
        'Accessoires':list_produit.filter(categorie='Accessoires').count(),
        'Maison':list_produit.filter(categorie='Home & Furnishings').count(), 
        'Art':list_produit.filter(categorie='Art & collections').count(),
        'Faits':list_produit.filter(typeProduit='Handmade').count(),
        'Vintage':list_produit.filter(typeProduit='Vintage').count(),
        'Standard':list_produit.filter(pour='standard').count(), 
        'bebe':list_produit.filter(pour='baby').count(), 
        'enfant':list_produit.filter(pour='child').count(),
        'jeune':list_produit.filter(pour='young').count(), 
        'adulte':list_produit.filter(pour='adult').count(),
    }  
    return render(request, 'discover/discover.html',context) 

  


def filter2(request):
    counter2=[]
    if request.user.is_authenticated():    
        user = request.user
        counter2 = Wishlist.objects.filter(user=user)
    
    catego = request.GET.get("catego","")
    creat = request.GET.get("creat","")
    print (creat)
    #prixx = request.GET.get("prixx","")
    genre = request.GET.get("Genre","")
    pour = request.GET.get("pour","")
    print(pour)
    #valeur = request.GET.get("rangeInput",'10,1000')
   # print(valeur[0])
    print('ok')
    print (genre)
    type0 = request.GET.get("type0","")
    recherche = request.GET.get("recherche","")
    produit_results = Produit.objects.filter(is_favorite=True)
    #valeur=valeur.split(',')
    #min0=int(valeur[0])
   #max0=int(valeur[1])
    minprice = request.GET.get("minprice","10")
    maxprice = request.GET.get("maxprice","1000")
    #tags = request.GET.get("tags")
   



    if recherche:
        tags_list = recherche.split(', ')
        tags_list = list(filter(None, tags_list))
       # print("recherche .... : " + str(recherche))
        produit_results = Produit.objects.filter(
               Q(title__contains=recherche) | Q(descreption__contains=recherche) | Q(tags__name__in=tags_list)).distinct()
    #if tags:
        
     #   produit_results = produit_results.filter(tags__name__in=tags_list).distinct()


    if catego and (catego != "All products" ):
        produit_results = produit_results.filter(Q(categorie__contains=catego)
                                                 ).distinct()

        
    if type0:
    
        produit_results = produit_results.filter(
             Q(typeProduit__contains=type0)
        ).distinct()
    
    if minprice :
        produit_results = produit_results.filter(
             Q(prix__lte=maxprice)&Q(prix__gte=minprice)
            ).distinct()   
           

    if creat=='croissant':
        produit_results =  produit_results.order_by('-created')
    if creat=='decroissant':     
        produit_results =  produit_results.order_by('created')
    if creat=='croissant1':
        produit_results =  produit_results.order_by('prix')
    if creat=='decroissant2':     
        produit_results =  produit_results.order_by('-prix')
    
    if genre :
        produit_results = produit_results.filter(Q(Genre=genre)
                                                 ).distinct()
    if pour:
    
        produit_results = produit_results.filter(
             Q(pour__contains=pour)
        ).distinct()                                             
        print(produit_results)

    if (catego =="All products"):
        produit_results=Produit.objects.filter(is_favorite=True)
        
    price = "&minprice="+str(minprice)+"&maxprice="+str(maxprice)
    filters = "creat="+str(creat)+"&catego="+str(catego)+"&recherche="+str(recherche)+"&type="+str(type0)+"&genre="+str(genre)+"&pour="+str(pour)+price
    paginator = Paginator(produit_results,8)
    page = request.GET.get('page')
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)

        
    context={
        'counter2':counter2,
        'filters':filters,
        'page':page, 
        'minx': min([post['prix']  for post in Produit.objects.all().values('prix')] ),
        'maxx' : max([post['prix'] for post in Produit.objects.all().values('prix')]),   
        'produits': produits, 
        'Tous':Produit.objects.filter(is_favorite=True).count(), 
        'Bijoux':produit_results.filter(categorie='Jewelry').count(), 
        'Vetement':produit_results.filter(categorie='Clothes').count(), 
        'Accessoires':produit_results.filter(categorie='Accessoires').count(),
        'Maison':produit_results.filter(categorie='Home & Furnishings').count(), 
        'Art':produit_results.filter(categorie='Art & collections').count(),
        'Faits':produit_results.filter(typeProduit='Handmade').count(),
        'Vintage':produit_results.filter(typeProduit='Vintage').count(),
        'categorie' :catego,
        'Standard':produit_results.filter(pour='standard').count(), 
        'bebe':produit_results.filter(pour='baby').count(), 
        'enfant':produit_results.filter(pour='child').count(),
        'jeune':produit_results.filter(pour='young').count(), 
        'adulte':produit_results.filter(pour='adult').count(),
    }
    print(context['maxx'])
    print(context['minx'])
    return render(request, 'discover/discover.html', context)



@ajax_required
def auto(request):
    produits = Produit.objects.filter(is_favorite=True)
    dump = []
    template = '{0} ({1})'
    for produit in produits:        
        dump.append(produit.title)
                                              
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


def search(request):
    produit_results = Produit.objects.filter(is_favorite=True)
    recherche = request.GET.get("recherche")
    #tags = request.GET.get("tags")
    catego = request.GET.get("catego","")
    creat = request.GET.get("creat","")
    print (creat)
    #prixx = request.GET.get("prixx","")
    genre = request.GET.get("Genre", "")
    pour = request.GET.get("pour", "")
    type0 = request.GET.get("type0", "")
    minprice = request.GET.get("minprice","10")
    maxprice = request.GET.get("maxprice","1000")
    

    print(recherche)

       # print("recherche .... : " + str(recherche))
    if recherche :    
        tags_list = recherche.split(', ')
        tags_list = list(filter(None, tags_list))
        produit_results = Produit.objects.filter(
               Q(title__contains=recherche) | Q(descreption__contains=recherche) | Q(tags__name__in=tags_list)).distinct()
  
    #if tags:
    #    tags_list = tags.split(', ')
    #    tags_list = list(filter(None, tags_list))
       # produit_results = produit_results.filter(tags__name__in=tags_list).distinct()
    price = "&minprice="+str(minprice)+"&maxprice="+str(maxprice)
    filters = "creat="+str(creat)+"&catego="+str(catego)+"&recherche="+str(recherche)+"&type="+str(type0)+"&genre="+str(genre)+"&pour="+str(pour)+price
    paginator = Paginator(produit_results,8)
    page = request.GET.get('page')
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)

        
    context={
        'filters':filters,
        'page':page, 
        'minx': min([post['prix']  for post in Produit.objects.all().values('prix')] ),
        'maxx': max([post['prix'] for post in Produit.objects.all().values('prix')]),
        'produits': produits, 
        'Tous':Produit.objects.filter(is_favorite=True).count(), 
        'Bijoux':produit_results.filter(categorie='Jewelry').count(), 
        'Vetement':produit_results.filter(categorie='Clothes').count(), 
        'Accessoires':produit_results.filter(categorie='Accessoires').count(),
        'Maison':produit_results.filter(categorie='Home & Furnishings').count(), 
        'Art':produit_results.filter(categorie='Art & collections').count(),
        'Faits':produit_results.filter(typeProduit='Handmade').count(),
        'Vintage':produit_results.filter(typeProduit='Vintage').count(),
        'Standard':produit_results.filter(pour='standard').count(), 
        'bebe':produit_results.filter(pour='baby').count(), 
        'enfant':produit_results.filter(pour='child').count(),
        'jeune':produit_results.filter(pour='young').count(), 
        'adulte':produit_results.filter(pour='adult').count(),
        
    }
    return render(request, 'discover/discover.html', context)
	

def boutique(request, pk):
    user = request.user
    counter2=[]
    if request.user.is_authenticated():   
        counter2 = Wishlist.objects.filter(user=user)

    product = Produit.objects.get(pk=pk)
    produit_results = Produit.objects.filter(boutique_id = product.boutique.id)
    boutique = get_object_or_404(Boutique, pk=product.boutique.id)
    commercant = get_object_or_404(Utilisateur, user=product.boutique.user)
    #album = get_object_or_404(Album, utilisateur=product.boutique.user)
    if not boutique.visitors.filter(pk=request.user.id).exists() and request.user.is_authenticated() and boutique.user !=request.user :
            boutique.visitors.add(request.user)
            Message.send_message(from_user=boutique.user, to_user=request.user, message=commercant.message)
    print(commercant)
    paginator = Paginator(produit_results,8)
    page = request.GET.get('page')
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)
    return render(request, 'discover/produitsBoutique.html', {'counter2':counter2,'page':page,'produits':produits,'boutique': boutique,'commercant':commercant})


def products(request):
    counter2=[]
    user = request.user
    if request.user.is_authenticated():   
        counter2 = Wishlist.objects.filter(user=user)
    produits = Produit.objects.all()
    produits = produits.filter().order_by('-created')[:4]
    posts = Post.objects.all()
    posts = posts.filter().order_by('-date')[:4]

    context={
        'counter2':counter2,
        'produits': produits, 
        'posts' : posts,
       
    }  
    return render(request, 'discover/PostProduct.html',context) 


    # tags = request.GET.get('tags')
    #    if tags:
    #     tags_list = tags.split(', ')
    #     tags_list = list(filter(None, tags_list))
    #     product_list = product_list.filter(tags__name__in=tags_list).distinct()
    #     tags_obj = Tag.objects.filter(name__in=tags_list).distinct()
    #     search_url = "{}tags={}&".format(search_url, tags)
    #     params['tags'] = tags