from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'Main/home.html')

def dashboard(request):
    return render(request, 'Main/dashboard.html')

def discussion(request):
    return render(request, 'Main/discussion.html')

def groupchat(request):
    return render(request, 'Main/groupchat.html')

def signin(request):
    return render(request, 'Main/signin.html')

