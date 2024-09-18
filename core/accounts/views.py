from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegisterForm
from .models import ShopUser

# Create your views here.

def log_out(request):
    logout(request)
    return redirect('shop:product_list')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form':form})


