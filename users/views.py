from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm
from .models import CustomUser

def register(request):
    """
    Handles user registration.
    - On POST: Validates form, creates user, and logs them in.
    - On GET: Displays empty registration form.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with your target URL
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    """Custom login view using the users/login.html template."""
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    """Custom logout view that redirects to the homepage after logout."""
    next_page = 'home'  # Replace 'home' with your target URL