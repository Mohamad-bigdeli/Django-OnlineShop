from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .forms import RegisterForm, EditUserForm
from .models import ShopUser
from django.contrib.auth.decorators import login_required

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

@login_required
def edit_user(request):
    user = get_object_or_404(ShopUser, id=request.user.id)
    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.phone = cd['phone']
            user.address = cd['address']
            user.save()
            return redirect('shop:product_list')
    else:
        form = EditUserForm()
    return render(request, 'registration/edit_user.html', {'form':form})