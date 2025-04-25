from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

def home(request):
    return render(request, 'Main/home.html')

def signin_view(request):
    return render(request, 'Main/signin.html')

def dashboard(request):
    return render(request, 'Main/dashboard.html')

def discussion(request):
    return render(request, 'Main/discussion.html')

def groupchat(request):
    return render(request, 'Main/groupchat.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
           if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')
           elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')
           elif len(username) < 4:
                messages.error(request, 'Username must be at least 5 characters long.')
                return redirect('register')
           elif len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('register')
           elif not any(char.isdigit() for char in password):
                messages.error(request, 'Password must contain at least one digit.')
                return redirect('register')
           else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('signin')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
      
        return render(request, 'Main/register_success.html', {'username': username})
    
    else:
        return render(request, 'Main/register.html')
