from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Profile
# Create your views here.

def home(request):
    return render(request, 'Main/home.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('signin')

    return render(request, 'Main/signin.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'Main/dashboard.html')

@login_required
def discussion(request):
    return render(request, 'Main/discussion.html')

@login_required
def groupchat(request):
    return render(request, 'Main/groupchat.html')

@login_required
def settings(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        profile.bio = request.POST.get('bio')
        profile.gender = request.POST.get('gender')
        profile.major = request.POST.get('major')
        profile.minor = request.POST.get('minor')
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('settings')
    return render(request, 'Main/settings.html', {'user': user, 'profile': profile})

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
