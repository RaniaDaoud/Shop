from __future__ import unicode_literals
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post, Categorie, Comment
from post.forms import PostForm ,CommentForm
from django.http import HttpResponse
from projet3.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views import generic
from notification.models import Notification




@login_required
def posts(request):
    user = request.user
    posts = Post.objects.filter(user = user)
    categories = Categorie.objects.all()
    return render(request,'post/post.html',{'posts':posts,'categories':categories, 'form': PostForm()})


@login_required
@ajax_required
def post(request):
    if request.method == 'POST':
        #post = request.POST.get('post')
        #categorie = request.POST.get('categorie')
        

        
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            #obj.image = request.FILES['image']
            #post = Post.send_post(user, post, categorie, image=obj)                        
            obj.save()
            
            # else:
            #     post = Post.send_post(user, post, categorie)
            #     print('form is invalid')

            return render(request, 'post/partial_post.html', {'post': obj,'form':form})
    else:
        print('This is a bad request inside post view')
        return HttpResponseBadRequest()


  
def post_posts(request):
     
    posts = Post.objects.all()
    paginator = Paginator(posts,8)
    page = request.GET.get('page')
    try:
        liste= paginator.page(page)
    except PageNotAnInteger:
        liste = paginator.page(1)
    except EmptyPage:
        liste = paginator.page(paginator.num_pages)

    context={
        
        'page':page,
        'posts' :posts,
        
        'liste_posts' : liste,
        'Tous':Post.objects.all().count(), 
        'Bijoux':Post.objects.all().filter(categorie__name='Bijoux').count(), 
        'Vetement':Post.objects.all().filter(categorie__name='vetement').count(), 
        'Accessoires':Post.objects.all().filter(categorie__name='accessoire').count(),
        'Maison':Post.objects.all().filter(categorie__name='meuble').count(), 
        'Art':Post.objects.all().filter(categorie__name='arts et collections').count(),
    }  
    return render(request, 'post/Discover_posts.html',context)

def post_detail_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        
        form = CommentForm(request.POST or None)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.user = request.user
            obj.save()
        #print(post)
        #comments = Comment.objects.filter(post_id=post_id)
        #print(comments)
        return render(request, 'post/detailPost.html', {'post': post,'form':form})
    return render(request, 'post/detailPost.html', {'post': post,'form':CommentForm()})

def post_comment_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        
        form = CommentForm(request.POST or None)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.user = request.user
            obj.save()
            print(obj)
        #comments = Comment.objects.filter(post_id=post_id)
        #print(comments)
        if post.user != request.user:
            Notification.send(from_user=request.user, to_user=post.user, type='comment', post=post)

        return render(request, 'post/comment.html', {'comment':obj})
    return render(request, 'post/form_comment.html', {'form':CommentForm()})


def searchPost(request):
    posts1 = Post.objects.all()
    post_results = Post.objects.all()
    recherche = request.GET.get("recherche1")
    print(recherche)
    catego = request.GET.get("categorie1","")

       # print("recherche .... : " + str(recherche))
      
    post_results = Post.objects.filter(
               Q(post__icontains=recherche) | Q(categorie__name__icontains=recherche)).distinct()
  
    if catego and (catego != "" ):
        post_results = post_results.filter(Q(categorie__name__contains=catego)
                                                  ).distinct()

    filters = "catego="+str(catego)+"&recherche="+str(recherche)

    paginator = Paginator(post_results,8)
    page = request.GET.get('page')
    try:
        posts= paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

        
    context={
        
        'page':page, 
        'posts' : posts1,
        'posts': posts, 
        'filtersPost' :filters,
        'Tous':Post.objects.all().count(), 
        'Bijoux':post_results.filter(categorie__name='Bijoux').count(), 
        'Vetement':post_results.filter(categorie__name='vetement').count(), 
        'Accessoires':post_results.filter(categorie__name='accessoire').count(),
        'Maison':post_results.filter(categorie__name='meuble').count(), 
        'Art':post_results.filter(categorie__name='arts et collections').count(),
        
        
    }
    return render(request, 'post/Discover_posts.html', context)      