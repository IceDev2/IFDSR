from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['judul', 'isi', 'gambar']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul post'}),
            'isi': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Tulis sesuatu...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['isi']
        widgets = {
            'isi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tulis komentar...'}),
        }
