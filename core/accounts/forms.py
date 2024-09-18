from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShopUser
from django.contrib.auth.forms import AuthenticationForm

class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'address', 'is_active', 'is_staff', 'is_superuser', 'date_joined']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.isinstance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone already exist.')
        else:
            if ShopUser.objects.filter(phone=phone).exists(): 
                raise forms.ValidationError('Phone already exist.')
        if not phone.isdigit():
            raise forms.ValidationError('Invalid phone number.')
        if not phone.startwith('09'):
            raise forms.ValidationError('Phone must start with 09 digits.')
        if len(phone) != 11:
            raise forms.ValidationError('Phone must have 11 digits.')
        return phone

class ShopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'address', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone already exist.')
        else:
            if ShopUser.objects.filter(phone=phone).exists(): 
                raise forms.ValidationError('Phone already exist.')
        if not phone.isdigit():
            raise forms.ValidationError('Invalid phone number.')
        if not phone.startwith('09'):
            raise forms.ValidationError('Phone must start with 09 digits.')
        if len(phone) != 11:
            raise forms.ValidationError('Phone must have 11 digits.')
        return phone
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, label="Phone",
                            widget=forms.TextInput())
    password = forms.CharField(max_length=250, required=True, label="Password",
                            widget=forms.PasswordInput())
    
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="repeat password")

    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'phone']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone already exist.')
        else:
            if ShopUser.objects.filter(phone=phone).exists(): 
                raise forms.ValidationError('Phone already exist.')
        if not phone.isdigit():
            raise forms.ValidationError('Invalid phone number.')
        if not phone.startswith('09'):
            raise forms.ValidationError('Phone must start with 09 digits.')
        if len(phone) != 11:
            raise forms.ValidationError('Phone must have 11 digits.')
        return phone