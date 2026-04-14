from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email của bạn',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mật khẩu',
            'autocomplete': 'current-password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        }),
        label='Ghi nhớ đăng nhập'
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email của bạn'
        })
    )
    password1 = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mật khẩu'
        })
    )
    password2 = forms.CharField(
        label='Nhập lại mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nhập lại mật khẩu'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email này đã được đăng ký!')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            # Tạo profile cho user mới
            UserProfile.objects.create(user=user, role='customer')
        return user

