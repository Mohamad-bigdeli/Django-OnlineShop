from django.urls import path
from . import views

app_name = "cart"

url_patterns = [
    path('add/<int:product_id>/', views.add_to_cart, name="add_to_cart")
]