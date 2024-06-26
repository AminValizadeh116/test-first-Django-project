from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text', 'writer']


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='inter password')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='repeat password')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords are not matched!')
        return cd['password2']


class CreatePostForm(forms.ModelForm):
    image2 = forms.ImageField(label='image2', required=False)
    image1 = forms.ImageField(label='image1', required=False)

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time', 'category']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['job', 'date_of_birth', 'bio', 'photo']


class SearchForm(forms.Form):
    query = forms.CharField()
