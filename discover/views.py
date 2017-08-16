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
from django.http import HttpResponse, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required





IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class DetailView(generic.DetailView):
    model = Produit
   
    template_name = 'discover/detailProduit.html'
    

def post_list(request):
     
    list_produit = Produit.objects.all()
    paginator = Paginator(list_produit,8)
    page = request.GET.get('page')
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)

    context={
        
        'page':page, 
        'minx': min( [post['prix'] for post in list_produit.values('prix')] ),
        'maxx': max([post['prix'] for post in list_produit.values('prix')]),
        'produits': produits, 
        'Tous':Produit.objects.all().count(), 
        'Bijoux':list_produit.filter(categorie='Bijoux').count(), 
        'Vetement':list_produit.filter(categorie='Vetement').count(), 
        'Accessoires':list_produit.filter(categorie='Accessoires').count(),
        'Maison':list_produit.filter(categorie='Maison et ameublement').count(), 
        'Art':list_produit.filter(categorie='Art et collections').count(),
        'Faits':list_produit.filter(typeProduit='Faits à main').count(),
        'Vintage':list_produit.filter(typeProduit='Vintage').count(),
    }  
    return render(request, 'discover/test.html',context) 

  


def filter2(request):

    
    catego = request.GET.get("catego","Tous les produits")
    creat = request.GET.get("creat","")
    prixx = request.GET.get("prixx","")
    #valeur = request.GET.get("rangeInput",'10,1000')
   # print(valeur[0])

    type0 = request.GET.get("type0")
    recherche = request.GET.get("recherche")
    produit_results = Produit.objects.all()
    #valeur=valeur.split(',')
    #min0=int(valeur[0])
   #max0=int(valeur[1])
    minprice = request.GET.get("minprice")
    maxprice = request.GET.get("maxprice")



    if recherche:
       # print("recherche .... : " + str(recherche))
        produit_results = Produit.objects.filter(
               Q(title__contains=recherche) | Q(descreption__contains=recherche)).distinct()

    if catego and (catego != "Tous les produits" ):
        produit_results = produit_results.filter(Q(categorie__contains=catego)
                                                 ).distinct()

    if (catego =="Tous les produits"):
        produit_results=Produit.objects.all()
        
    if type0:
    
        produit_results = produit_results.filter(
             Q(typeProduit__contains=type0)
        ).distinct()
    
    if minprice :
        produit_results = produit_results.filter(
             Q(prix__lte=maxprice)&Q(prix__gte=minprice)
            ).distinct()

    
    #minx = min([post['prix']  for post in produit_results.values('prix')] )
    # maxx = max([post['prix'] for post in produit_results.values('prix')])
    #if minprice == maxprice :
        #minx = minp
        #maxx = maxp    

    if creat=='croissant':
        produit_results =  produit_results.order_by('-created')
    if creat=='decroissant':     
        produit_results =  produit_results.order_by('created')
    if creat=='croissant1':
        produit_results =  produit_results.order_by('prix')
    if creat=='decroissant2':     
        produit_results =  produit_results.order_by('-prix')
   

    filters = "creat="+str(creat)+"&catego="+str(catego)+"&recherche="+str(recherche)+"&type="+str(type0)+"&recherche="+str(recherche)
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
        'maxx' : max([post['prix'] for post in Produit.objects.all().values('prix')]),   
        'produits': produits, 
        'Tous':Produit.objects.all().count(), 
        'Bijoux':produit_results.filter(categorie='Bijoux').count(), 
        'Vetement':produit_results.filter(categorie='Vetement').count(), 
        'Accessoires':produit_results.filter(categorie='Accessoires').count(),
        'Maison':produit_results.filter(categorie='Maison et ameublement').count(), 
        'Art':produit_results.filter(categorie='Art et collections').count(),
        'Faits':produit_results.filter(typeProduit='Faits à main').count(),
        'Vintage':produit_results.filter(typeProduit='Vintage').count(),
        'categorie' :catego,
    }
    print(context['maxx'])
    print(context['minx'])
    return render(request, 'discover/test.html', context)



@ajax_required
def auto(request):
    produits = Produit.objects.all()
    dump = []
    template = '{0} ({1})'
    for produit in produits:        
        dump.append(produit.title)
                                              
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


def search(request):
    
    recherche = request.GET.get("recherche")
    print(recherche)

       # print("recherche .... : " + str(recherche))
    produit_results = Produit.objects.filter(
               Q(title__contains=recherche) | Q(descreption__contains=recherche)).distinct()
  
    paginator = Paginator(produit_results,8)
    page = request.GET.get('page')
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)

        
    context={
        
        'page':page, 
        'minx': min([post['prix']  for post in Produit.objects.all().values('prix')] ),
        'maxx': max([post['prix'] for post in Produit.objects.all().values('prix')]),
        'produits': produits, 
        'Tous':Produit.objects.all().count(), 
        'Bijoux':produit_results.filter(categorie='Bijoux').count(), 
        'Vetement':produit_results.filter(categorie='Vetement').count(), 
        'Accessoires':produit_results.filter(categorie='Accessoires').count(),
        'Maison':produit_results.filter(categorie='Maison et ameublement').count(), 
        'Art':produit_results.filter(categorie='Art et collections').count(),
        'Faits':produit_results.filter(typeProduit='Faits à main').count(),
        'Vintage':produit_results.filter(typeProduit='Vintage').count(),
        
    }
    return render(request, 'discover/discover.html', context)
	

def boutique(request, pk):

    product = Produit.objects.get(pk=pk)
    produit_results = Produit.objects.filter(boutique_id = product.boutique.id)
    boutique = get_object_or_404(Boutique, pk=product.boutique.id)
    commercant = get_object_or_404(Utilisateur, user=product.boutique.user)
    print(produit_results)
    paginator = Paginator(produit_results,8)
    page = request.GET.get('page')
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)
    return render(request, 'discover/produitsBoutique.html', {'page':page,'produits':produits,'boutique': boutique,'commercant':commercant})


def products(request):
     
    produits = Produit.objects.all()
    produits = produits.filter().order_by('-created')[:4]
    posts = Post.objects.all()
    posts = posts.filter().order_by('-date')[:4]

    context={
        
        'produits': produits, 
        'posts' : posts,
       
    }  
    return render(request, 'discover/PostProduct.html',context) 



      