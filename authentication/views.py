from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from authentication.forms import SignUpForm ,BusinessUserForm
from shop.models import Boutique, Produit
from .models import Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            welcome_post = '{0} has joined the network.'.format(user.username,
                                                                user.username)
            boutiques = Boutique.objects.filter(user=request.user)
            #return render(request, 'discover/discover.html', {'boutique': boutiques})
            return redirect ('/discover/produit/')
    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm()})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
               
                boutiques = Boutique.objects.filter(user=request.user)
                

                context={
                    'boutiques': boutiques,                    
                }  
                #return render(request, 'shop/index.html',context) 
                return redirect('/discover/produit/')
            else:
                return render(request, 'authentication/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'authentication/login.html', {'error_message': 'Invalid login'})
    return render(request, 'authentication/login.html')

def login_userM(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                return render(request,'messenger/new.html')
            else:
                return render(request, 'authentication/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'authentication/login.html', {'error_message': 'Invalid login'})
    return render(request, 'authentication/login.html')



def logout_user(request):
    logout(request)
    form = SignUpForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'authentication/login.html', context)



def utilisateur(request):
    print('test 2')
    if request.method == 'POST':
        form = BusinessUserForm(request.POST, request.FILES)

        if form.is_valid():
            print('test')
            fields = form.cleaned_data
            businessuser = Utilisateur(description=fields['description'], type=fields['type'],telephone=fields['telephone'])
            businessuser.user = request.user
            request.user.username = request.POST['username']
            request.user.save()
            businessuser.save()
            return redirect('/boutique/create_boutique/')
        else:
            print("aaaaaaaaaaa")
            return render(request, 'authentication/commercant.html', {'form': form})

    if not Utilisateur.objects.filter(user=request.user).exists():
        return render(request, 'authentication/commercant.html', {'form': BusinessUserForm()})
    return render(request, 'shop/create_boutique.html')     