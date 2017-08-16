from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, PasswordInput, FileInput, Select, CheckboxInput

from .models import Post ,Categorie, Comment

class PostForm(ModelForm):
	class Meta :
		model = Post
		fields =['categorie','post','image']
		
class CommentForm(ModelForm):
	class Meta :
		model = Comment
		fields =['text']