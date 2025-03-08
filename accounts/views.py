from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.db.models import Q

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'accounts/login.html')

    def post(self, request):
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Try to find user by username or email
        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
            user = authenticate(username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                messages.success(request, 'Successfully logged in!')
                return redirect('home')
            
        except User.DoesNotExist:
            pass
        
        messages.error(request, 'Invalid username/email or password.')
        return render(request, 'accounts/login.html')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'accounts/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate input
        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'accounts/register.html')

        # Check existing users
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'accounts/register.html')

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
            return render(request, 'accounts/register.html')
