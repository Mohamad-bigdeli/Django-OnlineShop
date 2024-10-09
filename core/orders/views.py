from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PhoneVerificationForm, OrderCreateForm
from accounts.models import ShopUser
from cart.cart import Cart
import random
from django.contrib.auth import login
from cart.common.KaveSms import send_sms_normal
from django.core.cache import cache
from .models import OrderItem
from django.contrib.auth.decorators import login_required

# Create your views here.

def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('orders:create_order')
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                messages.error(request, 'this phone is already registererd')
                return redirect('orders:verify_phone')
            else:
                tokens = {'token':''.join(random.choices('0123456789', k=6))}
                token = tokens['token']
                cache.set('token', token, timeout=300)
                cache.set('phone', phone, timeout=300)
                send_sms_normal(phone, f'code : {token}')
                print(f"code : {token}")
                messages.success(request, "verification code sent successfully.(300s)")
                return redirect('orders:verify_code')

    else:
        form = PhoneVerificationForm()
    return render(request, 'verify_phone.html', {'form':form})

def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            phone = cache.get('phone')
            verification_code = cache.get('token')
            if code == verification_code:
                user = ShopUser.objects.create(phone=phone)
                user.set_password('12345')
                send_sms_normal(phone, 'your password : 12345')
                login(request, user)   
                return redirect('orders:create_order')
            else:
                messages.error(request, 'Verification code is incorrect. ')

    return render(request, 'verify_code.html', )

@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                          quantity=item['quantity'], weight=item['weight'])
            cart.clear()    
            return redirect('shop:product_list')    
    else:
        form = OrderCreateForm()
    context = {
        'form' : form,
        'cart' : cart
    }
    return render(request, 'create_order.html', context)