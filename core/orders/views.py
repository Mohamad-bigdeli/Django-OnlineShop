from django.shortcuts import render, redirect
from django.http import HttpResponse
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
from django.conf import settings
import requests
import json

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
            order = form.save(commit=False)
            order.buyer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                          quantity=item['quantity'], weight=item['weight'])
            # cart.clear()    
            return redirect('orders:request')    
    else:
        form = OrderCreateForm()
    context = {
        'form' : form,
        'cart' : cart
    }
    return render(request, 'create_order.html', context)

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# Important: need to edit for real server.
CallbackURL = 'http://127.0.0.1:8080/verify/'


def send_request(request):
    cart = Cart(request)
    description = ""
    for item in cart:
        description += str(item['product'].name) + ", "
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": cart.get_final_price(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                cart.clear()
                return redirect(ZP_API_STARTPAY+authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(authority):
    data = {
        "MerchantID": settings.MERCHANT,
        # "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']
            if response['Status'] == 100:
                return HttpResponse(f'successful , RefID: {reference_id}')
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')