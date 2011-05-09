# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from authorization.models import MyUser

class SigninUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ("username", "email")
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            MyUser.objects.get(username = data)
            raise forms.ValidationError(u"Это имя уже занято")
        except MyUser.DoesNotExist:
            return data
    
    def clean_email(self):        
        data = self.cleaned_data['email']
        try:
            MyUser.objects.get(email = data)
            raise forms.ValidationError(u"Этот еmail уже занят")
        except MyUser.DoesNotExist:
            return data
            
class EditProfileForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length = 100, label='Имя пользователя')
    password = forms.CharField(max_length = 100, widget= forms.PasswordInput, required=False, label='Пароль')
    password2 = forms.CharField(max_length = 100, widget= forms.PasswordInput, required=False, label='Подтверждение пароля')
    first_name = forms.CharField(max_length = 100, required=False, label='Имя')
    last_name = forms.CharField(max_length = 100, required=False, label='Фамилия')
    
    def __init__(self, user=None, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.user:
            self.initial = {'email': user.email, 'username': user.username, 'first_name':user.first_name, 'last_name':user.last_name}
            
    def clean_username(self):        
        data = self.cleaned_data['username']
        if data ==  self.user.username:
            return data
        try:
            MyUser.objects.get(username = data)
            raise forms.ValidationError(u"Это имя уже занято")
        except MyUser.DoesNotExist:
            return data
    
    def clean_email(self):        
        data = self.cleaned_data['email']
        if data ==  self.user.email:
            return data
        try:
            MyUser.objects.get(email = data)
            raise forms.ValidationError(u"Этот еmail уже занят")
        except MyUser.DoesNotExist:
            return data
    
    def clean(self):
        cleaned_data = self.cleaned_data            
        if 'password' in cleaned_data or 'password2' in cleaned_data:            
            if 'password' in cleaned_data and 'password2' in cleaned_data:
                if cleaned_data['password'] != cleaned_data['password2']:
                    raise forms.ValidationError(u'Пароли не совпадают')
            else:
                raise forms.ValidationError(u'Either ener both or None of the password fields')                    
        return cleaned_data       
        
    def save(self):
        user = self.user
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if len(self.cleaned_data['password']) > 0:
                user.set_password(self.cleaned_data['password'])
        user.save()        
        return user