from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['user_type', 'name', 'mobile', 'gender', 'password1', 'password2']
        widgets = {
            'user_type':forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Full Name'}),
            'mobile':forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contact Number'}),
            'gender': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            # 'password1':forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
            # 'password2':forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Re-Password'})
        }
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your password'}),
        label='Password'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Repeat your password'}),
        label='Repeat Password'
    )

class CustomAuthenticationForm(AuthenticationForm):
    mobile = forms.CharField(max_length=20)
    # class Meta:
    #     model = User
    #     fileds = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget = forms.HiddenInput()
        self.fields['mobile'].widget.attrs.update({'autofocus': ''})

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')
        if mobile is not None and password:
            self.user_cache = authenticate(self.request, mobile=mobile, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
