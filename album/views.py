import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required 

from album.models import Photo
from album.forms import PhotoForm
from authentication.models import *
from album.models import *

from projet3.decorators import ajax_required

# def create_album(request):
#     if request.method == 'POST':
#         photos = request.user.utilisateur.album.photos.all()
#         photo = photos[0]
#         user =  photo.album.utilisateur.user
#         return render(request, 'album/album.html',{'photos':photos,'user':user})
#     return render(request, 'album/album.html')



def album(request, user_id) :   
    user = Utilisateur.objects.get(id=user_id)
    album = Album.objects.get(utilisateur=user)
    photos = Photo.objects.filter(album=album)
    print(user)
    return render(request,'album/album.html', {'photos':photos,'user':user})
    



def create_album(request):
    # if request.user.utilisateur :
    #     album = Album(utilisateur=request.user.utilisateur)
    #     album.save()
    #     # photos = request.user.utilisateur.album.photos.all()
    #     # photo = photos[0]
    #     # user =  photo.album.utilisateur.user

    #     return render(request, 'album/album.html')
    if request.method =='GET':
        if request.user.utilisateur.album :
            #album = Album(utilisateur=request.user.utilisateur)
            #album.save()   
            photos = request.user.utilisateur.album.photos.all()
           # photo = photos[0]
            user =  request.user.utilisateur
            #print(photo)
            return render(request, 'album/album.html',{'photos':photos,'user':user})
    else:
        album = Album(utilisateur=request.user.utilisateur)
        album.save()
        # photos = request.user.utilisateur.album.photos.all()
        # photo = photos[0]
        # user =  photo.album.utilisateur.user

        return render(request, 'album/album.html')
    return render(request, 'album/album.html')

@login_required
@ajax_required
def new_photo_view(request):
    photos = request.user.utilisateur.album.photos.all()    

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            print("form is valid")
            obj = form.save(commit=False)
            obj.album = request.user.utilisateur.album
            obj.save()
            return render(request, 'album/partial_photo.html', {'form': obj,'photos':photos})
        return HttpResponse(json.dumps({"failed": True}), content_type='application/json')
    else:
        return HttpResponseBadRequest()


@login_required
@ajax_required
def delete_photo_view(request, pk):
    if request.method == 'POST':
        print('ok')
        photo = Photo.objects.get(pk=pk)
        photo.delete()
        photos = request.user.utilisateur.album.photos.all() 
        #request.user.utilisateur.album.photos.get(pk=pk).delete()
    #return render(request, 'album/photo.html', {'photos': photos})
        
    return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    
