from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as User_Auth

# Create your forms here.

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    def save(self, commit=True):
        user_auth = super(NewUserForm, self).save(commit=False)
        user_auth.first_name = self.cleaned_data['first_name']
        user_auth.last_name = self.cleaned_data['last_name']
        user_auth.email = self.cleaned_data['email']
        if commit:
            user_auth.save()
        return user_auth

    class Meta:
        fields = ("username", "first_name", "last_name", "email", "password1", "password2") 
        model = User_Auth
