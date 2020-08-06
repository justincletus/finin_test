from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(forms.ModelForm):
    mobile = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Add country code prefix'
        }
    ))
    re_password = forms.CharField(max_length=120, widget=PasswordInput, label="Re-enter Password")

    def __init__(self, *args, **kargs):
        super(SignupForm, self).__init__(*args, **kargs)
      
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',       
            'email',
            'mobile',
            'password',
            're_password'
        ]
        widgets = {
            'password': PasswordInput(),
            're_password': PasswordInput()
        }
    

class MyAuthForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput(attrs={
        'placeholder': 'Email Id'
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Password'
    }))
                  
        
