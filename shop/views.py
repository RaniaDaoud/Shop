import json
from projet3.decorators import ajax_required
from django.views.decorators.csrf import requires_csrf_token
from .models import Boutique, Produit
from .forms import BoutiqueForm,  ProduitForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.models import Utilisateur
from authentication.forms import BusinessUserForm

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
    template_name = 'shop/detailProduit.html'
       


def detail(request, boutique_id):
    if not request.user.is_authenticated():
        return render(request, 'authentication/login.html')
    else:
        user = request.user
        boutique = get_object_or_404(Boutique, pk=boutique_id)
        commercant = get_object_or_404(Utilisateur, user=boutique.user)
        return render(request, 'shop/detailBoutique.html', {'boutique': boutique, 'user': user, 'commercant':commercant})

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'authentication/login.html')
    else:
        boutiques = Boutique.objects.filter(user=request.user)
        produit_results = Produit.objects.all()
        query = request.GET.get("q")
        if query:
            boutiques = boutiques.filter(
                Q(name__icontains=query)

            ).distinct()
            produit_results = produit_results.filter(
                Q(title__icontains=query) |  Q(descreption__icontains=query)
            ).distinct()
            return render(request, 'shop/index.html', {
                'boutiques': boutiques,
                'produits': produit_results,
            })
        else:
            return render(request, 'shop/index.html', {'boutiques': boutiques})


def create_boutique(request):
    if not request.user.is_authenticated():
        return render(request, 'authentication/login.html')
    else:
        form = BoutiqueForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            boutique = form.save(commit=False)
            boutique.user = request.user
            boutique.logo = request.FILES['logo']
            file_type = boutique.logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'boutique': boutique,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'shop/create_boutique.html', context)
            boutique.save()
            return render(request, 'shop/index.html', {'boutique': boutique})
        context = {
            "form": form,
        }
        return render(request, 'shop/create_boutique.html', context)


def delete_boutique(request, boutique_id):
    boutique = Boutique.objects.get(pk=boutique_id)
    boutique.delete()
    boutiques = Boutique.objects.filter(user=request.user)
    return render(request, 'shop/index.html', {'boutique': boutiques})


@requires_csrf_token
def create_produit(request, boutique_id):
    if(request.method == 'POST'):
        form = ProduitForm(request.POST or None, request.FILES or None)
        boutique = get_object_or_404(Boutique, pk=boutique_id)
        if form.is_valid():
            boutiques_produits = boutique.produit_set.all()
            for s in boutiques_produits:
                if s.title == form.cleaned_data.get("title"):
                    context = {
                        'boutique': boutique,
                        'form': form,
                        'error_message': 'You already added that product',
                    }
                    return render(request, 'shop/create_produit.html', context)
            produit = form.save(commit=False)
            produit.boutique = boutique

            produit.save()
            return render(request, 'shop/detailBoutique.html', {'boutique': boutique})
    else:
        form = ProduitForm()
        boutique = get_object_or_404(Boutique, pk=boutique_id)
        context = {
            'boutique': boutique,
            'form': form,
        }
        return render(request, 'shop/create_produit.html', context)

def delete_produit(request, boutique_id, produit_id):
    boutique = get_object_or_404(Boutique, pk=boutique_id)
    produit = Produit.objects.get(pk=produit_id)
    produit.delete()
    return render(request, 'shop/detailBoutique.html', {'boutique': boutique})


def favorite(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    try:
        if produit.is_favorite:
            produit.is_favorite = False
        else:
            produit.is_favorite = True
        produit.save()
    except (KeyError, Produit.DoesNotExist):
        return JsonResponse({'success': False})
        
        
    else:
        return JsonResponse({'success': True})
        



def dupliquer(request,  produit_id):
   
    produit = Produit.objects.get(pk=produit_id)
    produit.id = None
    produit.save()
  #  print ('success')
    return redirect('/boutique/detail/'+str(produit.boutique.id))


def post_update(request, produit_id):
    instance = get_object_or_404(Produit, id=produit_id)
    form = ProduitForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        #instance.logo = form.cleaned_data["logo"]
        #instance.logo1 = form.cleaned_data["logo1"]
        instance.logo1 = request.POST.get('logo1') or instance.logo1
        instance.logo2 = request.POST.get('logo2') or instance.logo2
        instance.logo3 = request.POST.get('logo3') or instance.logo3
        instance.save()
        return HttpResponseRedirect('/boutique/detail/'+str(instance.boutique.id))   
    context = {

    "form" : form,

   
    }    
    return render(request, "shop/create_produit.html", context)



# def post_listNO(request):
       
#     list_produit = Produit.objects.all()
#     paginator = Paginator(list_produit,8)
#     page = request.GET.get('page')
#     try:
#         produits= paginator.page(page)
#     except PageNotAnInteger:
#         produits = paginator.page(1)
#     except EmptyPage:
#         produits = paginator.page(paginator.num_pages)

#     context={
        
#         'page':page, 
#         'minx': min( [post['prix'] for post in list_produit.values('prix')] ),
#         'maxx': max([post['prix'] for post in list_produit.values('prix')]),
#         'produits': produits, 
#         'Tous':Produit.objects.all().count(), 
#         'Bijoux':list_produit.filter(categorie='Bijoux').count(), 
#         'Vetement':list_produit.filter(categorie='Vetement').count(), 
#         'Accessoires':list_produit.filter(categorie='Accessoires').count(),
#         'Maison':list_produit.filter(categorie='Maison et ameublement').count(), 
#         'Art':list_produit.filter(categorie='Art et collections').count(),
#         'Faits':list_produit.filter(typeProduit='Faits à main').count(),
#         'Vintage':list_produit.filter(typeProduit='Vintage').count(),
#     }  
#     return render(request, 'produit/Discover.html',context) 
#     


def post_updateBoutique(request, Boutique_id):
    instance = get_object_or_404(Boutique, id=Boutique_id)
    form = BoutiqueForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        #instance.logo = form.cleaned_data["logo"]
        #instance.logo1 = form.cleaned_data["logo1"]
        
        instance.save()
        return HttpResponseRedirect('/boutique/detail/'+str(instance.id))   
    context = {

    "form" : form,

   
    }    
    return render(request, "shop/create_boutique.html", context)

def post_updateUser(request, Boutique_id):
    instance = get_object_or_404(Utilisateur, id=Boutique_id)
    if request.method == 'POST':
        
        form = BusinessUserForm(request.POST or None, instance=instance)
        if form.is_valid():
            print('test')
            instance = form.save(commit=False)
            #instance.telephone = request.POST.get('telephone') or instance.telephone
            #instance.Description = request.POST.get('description') or instance.description
            #instance.logo = form.cleaned_data["logo"]
            #instance.logo1 = form.cleaned_data["logo1"]
            
            instance.save()
            return HttpResponseRedirect('/boutique/detail/'+str(instance.id))   
        context = {

        "form" : form,

       
        }    
        return render(request, "authentication/commercant.html", context) 
    else:
        form = BusinessUserForm( instance=instance)
        return render(request, "authentication/commercant.html", {"form" : form})
           