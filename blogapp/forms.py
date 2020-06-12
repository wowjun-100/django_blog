from django import forms
from .models import Blog, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CreateBlog(forms.ModelForm):
    class Meta:
        model = Blog

        fields = ['title', 'author', 'body', 'password']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '제목을 입력하세요.'}
            ),
            'author': forms.Select(
                attrs={'class': 'custom-select'},
            ),
            'body': forms.CharField(
                widget=CKEditorUploadingWidget()
            ),
            'password': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '패스워드를 입력하세요.'}
            ),
        }

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['comment_user', 'comment_thumbnail_url','comment_textfield', 'comment_password']

        widgets = {
            'comment_user': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '이름을 입력하세요.'}
            ),
            'comment_thumbnail_url': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '썸네일 주소를 입력하세요.'}
            ),
            'comment_textfield': forms.Textarea(attrs={"class": 'form-control', 'rows': 4, 'cols':40}
            ),
            'comment_password': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '패스워드를 입력하세요.'}
            ),
        }

class EditBlog(forms.ModelForm):
    class Meta:
        model = Blog

        fields = ['title', 'author', 'body', 'password']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '제목을 입력하세요.'}
            ),
            'author': forms.Select(
                attrs={'class': 'custom-select'},
            ),
            'body': forms.CharField(
                widget=CKEditorUploadingWidget()
            ),
            'password': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'type': 'password'}
            ),
        }