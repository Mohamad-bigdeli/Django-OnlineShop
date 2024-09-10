from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from django.http import JsonResponse

# Create your views here.

@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price()
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'error': "InvalidRequest"})
    
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart':cart})

@require_POST
def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(product)
        elif action == 'decrase':
            cart.decrase(product)
        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'success': True, 
            'quantity': cart.cart[item_id]['quantity'],
            'price': cart.cart[item_id]['price'],
            'total': cart.cart[item_id]['quantity'] * cart.cart[item_id]['price'],
            'final_price': cart.get_final_price(),
        }  
        return JsonResponse(context)  
    except:
        return JsonResponse({'success':False, 'error':"ItemNotFound"})