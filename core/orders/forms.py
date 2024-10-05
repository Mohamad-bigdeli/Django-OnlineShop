from django import forms
from accounts.models import ShopUser
from .models import Oreder

class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(max_length=11)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise forms.ValidationError('Invalid phone number.')
        if not phone.startswith('09'):
            raise forms.ValidationError('Phone must start with 09 digits.')
        if len(phone) != 11:
            raise forms.ValidationError('Phone must have 11 digits.')
        return phone
    
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Oreder
        fields = ['first_name', 'last_name', 'phone', 'address', 'postal_code', 'province', 'city']