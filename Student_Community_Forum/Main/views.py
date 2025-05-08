from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Profile, Discussion, Comment, Groupchat, Message
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
    user = request.user
    profile = Profile.objects.get(user=user)

    recent_discussions = Discussion.objects.all().order_by('-created_at')[:4]
    recent_groupchats = Groupchat.objects.all().order_by('-created_at')[:4]

    recent_comments = []
    for discussion in recent_discussions:
        latest_comment = Comment.objects.filter(discussion=discussion).order_by('-created_at').first()
        if latest_comment:
            recent_comments.append(latest_comment)


    return render(request, 'Main/dashboard.html', {
        'recent_discussions': recent_discussions, 
        'user': user, 'profile': profile, 
        'recent_groupchats': recent_groupchats, 
        'recent_comments': recent_comments
    })

#handles discussions, if none exists automatically creates one that welcomes user to forum
@login_required
def discussion(request):
    if not Discussion.objects.exists():
        Discussion.objects.create(title="Welcome to the Forum!", created_by=request.user)

    discussions = Discussion.objects.all()
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'Main/discussion.html', {
        'discussions': discussions,
        'profile': profile
    })

#handles discussion comments and posting comments
@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Handle new comment submission
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                discussion=discussion,
                user=request.user,
                content=content
            )
            return redirect('discussion_detail', discussion_id=discussion.id)

    # Get all comments for this discussion
    comments = Comment.objects.filter(discussion=discussion).order_by('created_at')


    return render(request, 'Main/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments,
        'user': request.user,
        'profile': profile
    })

#handles creating a new discussion
@login_required
def creatediscussion(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Discussion.objects.create(title=title, created_by=request.user)
            return redirect('discussion')  # after creating, go back to list
        
    return render(request, 'Main/creatediscussion.html', {
    'profile': profile
    })


@login_required
def groupchat(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    groupchats = Groupchat.objects.all()


    return render(request, 'Main/groupchat.html', {'groupchats': groupchats, 'profile': profile, 'user': user})

@login_required
def create_groupchat(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if Groupchat.objects.filter(title=title).exists():
            messages.error(request, "A group chat with this title already exists.")
            return redirect('create_groupchat')

        if title:
            groupchat = Groupchat.objects.create(
                title=title,
                created_by=user,
                description=description
            )
            groupchat.members.add(user)
            return redirect('groupchat_room', groupchat_id=groupchat.id)
    return render(request, 'Main/create_groupchat.html', {'profile': profile, 'user': user})

@login_required
def join_groupchat(request, groupchat_id):
    groupchat = get_object_or_404(Groupchat, id=groupchat_id)
    groupchat.members.add(request.user)

    return redirect('groupchat')

@login_required
def groupchat_room(request, groupchat_id):
    user= request.user
    profile = Profile.objects.get(user=user)
    groupchat = get_object_or_404(Groupchat, id=groupchat_id)
    messages = groupchat.messages.all().order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                groupchat=groupchat,
                sender=request.user,
                content=content
            )
            return redirect('groupchat_room', groupchat_id=groupchat.id)

    return render(request, 'Main/groupchat_room.html', {
        'profile': profile,
        'user': user,
        'groupchat': groupchat,
        'messages': messages
    })


@login_required
def leave_groupchat(request, groupchat_id):
    groupchat = get_object_or_404(Groupchat, id=groupchat_id)
    groupchat.members.remove(request.user)

    return redirect('groupchat')

@login_required
def delete_groupchat(request, groupchat_id):
    groupchat = get_object_or_404(Groupchat, id=groupchat_id)
    if request.user == groupchat.created_by:
        groupchat.delete()
        messages.success(request, "Group chat deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this group chat.")
    return redirect('groupchat')


@login_required
def settings(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')

        profile.bio = request.POST.get('bio')
        profile.gender = request.POST.get('gender')
        profile.major = request.POST.get('major')
        profile.minor = request.POST.get('minor')
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('settings')
    return render(request, 'Main/settings.html', {'user': user, 'profile': profile})

def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'Main/view_profile.html', {
        'user': user,
        'profile': profile
    })

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
