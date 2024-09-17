from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from accounts.models import ShopUser

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()  
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    context = {
        'products' : products,
        'category' : category,
        'categories' : categories
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, slug=slug, id=id)
    context = {
        'product' : product 
    }
    return render(request, 'shop/product_detail.html', context)