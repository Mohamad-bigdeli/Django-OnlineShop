from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm, template_name='registration/login.html'), name="login"),
    path('logout/', views.log_out, name="logout"),
    path('register/', views.register, name="register"),
    path('edit_user/', views.edit_user, name="edit_user"),   
]