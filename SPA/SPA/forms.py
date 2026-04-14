from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from services.models import CustomerProfile


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "placeholder": "Nhap email cua ban",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        label="Mat khau",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Nhap mat khau",
                "required": True,
            }
        ),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "placeholder": "Nhap email cua ban",
                "required": True,
            }
        ),
    )
    first_name = forms.CharField(
        label="Ten",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Nhap ten cua ban",
                "required": True,
            }
        ),
    )
    last_name = forms.CharField(
        label="Ho",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Nhap ho cua ban",
                "required": False,
            }
        ),
    )
    password1 = forms.CharField(
        label="Mat khau",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Nhap mat khau (it nhat 8 ky tu)",
                "required": True,
            }
        ),
    )
    password2 = forms.CharField(
        label="Xac nhan mat khau",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Nhap lai mat khau",
                "required": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email nay da duoc dang ky. Vui long su dung email khac.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Mat khau khong khop.")
        return password2


class CustomerProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        label="Ho va ten",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "account-input",
                "placeholder": "Nhap ho va ten",
            }
        ),
    )

    class Meta:
        model = CustomerProfile
        fields = ("full_name", "phone", "birth_date", "address", "notes")
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "account-input",
                    "placeholder": "Nhap so dien thoai",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "account-input",
                    "type": "date",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "account-input",
                    "placeholder": "Nhap dia chi",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "account-input account-textarea",
                    "rows": 3,
                    "placeholder": "Thong tin suc khoe, so thich dieu tri, luu y dac biet...",
                }
            ),
        }
