from django.urls import path
from .views import register, CustomLoginView, CustomLogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]