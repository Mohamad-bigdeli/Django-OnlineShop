from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('verify_phone/', views.verify_phone, name="verify_phone"),
    path('verify_code/', views.verify_code, name="verify_code"),
    path('create_order/', views.create_order, name="create_order"),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
    path('orders_list/', views.orders_list, name="orders_list")
]