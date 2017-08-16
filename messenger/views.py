import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from projet3.decorators import ajax_required
from messenger.models import Message ,Attachement
from messenger.forms import AttachementForm
from shop.models import Produit
from authentication.models import Utilisateur
from authentication.forms import  BusinessUserForm



@login_required
def inbox(request):
    conversations = Message.get_conversations(user=request.user)
    to_user = request.GET.get('user')
    from_user = request.user 

    #print (to_user)
   # print (from_user.username)

    produits = Produit.objects.filter(boutique__user__username=to_user)
    #produitsU = Produit.objects.filter(boutique__user__username=from_user.username)[:3]
    if not Utilisateur.objects.filter(user=request.user).exists():
            produitsU = Produit.objects.all()[:3]
    if Utilisateur.objects.filter(user=request.user).exists():
            produitsU = Produit.objects.filter(boutique__user__username=from_user.username)[:3]
       
    active_conversation = None
    messages = None
    if conversations:
        conversation = conversations[0]
        active_conversation = conversation['user'].username
        messages = Message.objects.filter(user=request.user,
                                          conversation=conversation['user'])
        messages.update(is_read=True)
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0




    return render(request, 'messenger/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'active': active_conversation,
        'produits' :produits,
        'produitsU' :produitsU,
        
        })


#@login_required
def messages(request, username):
    if not request.user.is_authenticated():
        return render(request, 'shop/detailProduit.html')
    else:
        #to_user = request.GET.get('user') 


        from_user = request.user 
        #produitsU = Produit.objects.filter(boutique__user__username=from_user.username)[:3]

        produits = Produit.objects.filter(boutique__user__username=username)
        if not Utilisateur.objects.filter(user=request.user).exists():
            produitsU = Produit.objects.all()[:3]
        if Utilisateur.objects.filter(user=request.user).exists():
            produitsU = Produit.objects.filter(boutique__user__username=from_user.username)[:3]
       
        conversations = Message.get_conversations(user=request.user)
        active_conversation = username
        messages = Message.objects.filter(user=request.user,
                                          conversation__username=username)
        messages.update(is_read=True)
        for conversation in conversations:
            if conversation['user'].username == username:
                conversation['unread'] = 0
        
        
        return render(request, 'messenger/inbox.html', {
            'messages': messages,
            'conversations': conversations,
            'active': active_conversation ,
            'produits': produits,
            'produitsU': produitsU,
            
            })


#@login_required
def new(request):
    
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        objet = request.POST.get('objet')
        url = request.POST.get('url')
        if url:
            url=int(url)
            produit = Produit.objects.get(pk=url)
        else:
            url = None
            produit = None    
        
        try:
            to_user = User.objects.get(username=to_user_username)

        except Exception:
            try:
                to_user_username = to_user_username[
                    to_user_username.rfind('(')+1:len(to_user_username)-1]
                to_user = User.objects.get(username=to_user_username)

            except Exception:
                return redirect('/messages/new/')

        message = request.POST.get('message')
        #objet = request.POST.get('objet')
        #url = request.POST.get('url')
        #produit = Produit.objects.get(pk=url)
        if len(message.strip()) == 0:
            return redirect('/messages/new/')

        if from_user != to_user:
            Message.send_message(from_user, to_user, message, objet, produit)

        return redirect('/messages/{0}/?user={1}'.format(to_user_username,to_user_username))

    else:
        to = request.GET.get("username")
      #  print(to)
        produits = Produit.objects.filter(boutique__user__username=to)[:3]
        conversations = Message.get_conversations(user=request.user)
        return render(request, 'messenger/new.html',
                      {'conversations': conversations,'produits':produits})


@login_required
@ajax_required
def delete(request,message_id):
    conversations = Message.get_conversations(user=request.user)
    print(Hi)
    msg=Message.objects.get(id=message_id)
    print(done)
    msg.delete()

    
    return render(request, 'messenger/inbox.html',{'conversations': conversations})


@login_required
#@ajax_required
def send(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        print(to_user)
        message = request.POST.get('message')
        
        produitS = Produit.objects.filter(boutique__user__username=to_user)[:3]
       
        if len(message.strip()) == 0:
            return HttpResponse()
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user,  message=message,objet=None, produit=None)
            return render(request, 'messenger/includes/partial_message.html',
                          {'message': msg, 'produits' : produitS})
            #return HttpResponse(json.dumps({'message':msg.message,'produits' : dump}), content_type='application/json')

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@login_required
@ajax_required
def send_IMG(request):
    msg = None
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        print(to_user)
        message = request.POST.get('message')
       

        if from_user != to_user:
            form = AttachementForm(request.FILES)

            if form.is_valid():
                obj = form.save(commit=False)
                msg = Message.send_message(from_user, to_user, message, attachement=obj)
                obj.message = msg
                print(msg.attachement)
                obj.save()
                
            else:
                msg = Message.send_message(from_user, to_user, message)
                print('form is invalid')

        return render(request, 'messenger/includes/partial_message.html', {'message': msg})
    else:
        print('This is a bad request inside send view')
        return HttpResponseBadRequest()






@login_required
@ajax_required
def users(request):
    users = User.objects.filter(is_active=True)
    dump = []
    template = '{0} ({1})'
    for user in users:
        if user.profile.get_screen_name() != user.username:
            dump.append(template.format(user.profile.get_screen_name(),
                                        user.username))
        else:
            dump.append(user.username)
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


@login_required
@ajax_required
def check(request):
    count = Message.objects.filter(user=request.user, is_read=False).count()
    return HttpResponse(count)


def newM(request):
    
    if request.method == 'GET':
        from_user = request.user
        to_user_username = request.POST.get('to')
        
        try:
            to_user = User.objects.get(username=to_user_username)

        except Exception:
            try:
                to_user_username = to_user_username[
                    to_user_username.rfind('(')+1:len(to_user_username)-1]
                to_user = User.objects.get(username=to_user_username)

            except Exception:
                return redirect('/messages/new/')

        message = request.POST.get('message')
        #objet = request.POST.get('objet')
        #url = request.POST.get('url')
        #produit = Produit.objects.get(pk=url)
        if len(message.strip()) == 0:
            return redirect('/messages/new/')

        if from_user != to_user:
            Message.send_message(from_user, to_user, message, None, None)

        #return redirect('/messages/{0}/?user={1}'.format(to_user_username,to_user_username))
        return redirect('/messages/')
    else:
       
        conversations = Message.get_conversations(user=request.user)
        return render(request, 'messenger/new.html',
                      {'conversations': conversations})

        



'''@login_required

def sendP(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        print(to_user)
        message = request.POST.get('message')
        objet = request.POST.get('objet')
        url = request.POST.get('url')
        produit = Produit.objects.get(pk=url)
        
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message=message, objet=objet, produit=produit)
            return render(request, 'messenger/includes/partial_message.html',
                          {'message': msg})

        return HttpResponse()
    else:
        return HttpResponseBadRequest()'''
'''    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')
        objet = request.POST.get('objet')
        url = request.POST.get('url')
        produit = Produit.objects.get(pk=url)
        print(to_user)
        print(from_user)
        
        #objet = request.POST.get('objet')
        #url = request.POST.get('url')
        #produit = Produit.objects.get(pk=url)
        if len(message.strip()) == 0:
            return HttpResponse()
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message=message, objet=objet, produit=produit)
            # return render(request, 'messenger/includes/produit_user.html',
            #              {'message': msg})
            #return HttpResponse(json.dumps({'name': msg.message}), content_type='application/json')
       # else:
            return render(request, 'messenger/includes/partial_message.html',
                          {'message': msg})
            #return redirect('/messages/{0}/?user={1}'.format(to_user_username,to_user_username))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()    '''

@login_required

def sendMes(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        print(to_user)
        message = request.POST.get('message')
        objet = request.POST.get('objet')
        url = request.POST.get('url')
        produit = Produit.objects.get(pk=url)
        
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message=message, objet=objet, produit=produit)
            return render(request, 'messenger/includes/partial_message.html',
                          {'message': msg})

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def search(request):
    if request.method=='GET':
        from_user = request.user
        active= request.GET.get('to')
        recherche = request.GET.get("recherche")
        page = request.GET.get('page',1) 

        print('test')
        if recherche:
            
            if Utilisateur.objects.filter(user=request.user).exists():
                produit_results = Produit.objects.filter(boutique__user__username=from_user.username)
                
                   # print("recherche .... : " + str(recherche))
                produit_results = produit_results.filter( 
                           Q(title__contains=recherche) | Q(descreption__contains=recherche)).distinct()
            if not Utilisateur.objects.filter(user=request.user).exists():
                produit_results = Produit.objects.all()
                produit_results = produit_results.filter( 
                           Q(title__contains=recherche) | Q(descreption__contains=recherche)).distinct()

        else:
            produit_results = Produit.objects.all()

    else :
        print('None')


    print(recherche)
    print(produit_results)

    
    paginator = Paginator(produit_results,3)
    if page :
        page=int(page)
        if page <=0:
            page=1
        if page> paginator.num_pages:
            page= paginator.num_pages   

    
    
    
    try:
        produits= paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)
    print(produits)    

        
    context={
        'active' : active,
        'page':page, 
        'produitS': produits, 
        
    }

    data = {
        'produits': render_to_string('messenger/includes/search_result.html', context),
        'modals': render_to_string('messenger/includes/search_result_modals.html', context)
    }

    return HttpResponse(json.dumps(data), content_type='application/json')

    #return render(request, 'messenger/includes/search_result.html', context)        