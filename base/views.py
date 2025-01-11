from django import forms
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
import json
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdditionalPhoto, Profile
from django.db.models import Q
from channels.generic.websocket import WebsocketConsumer

def home(request):
    return render(request, 'base/home.html')

'''
@login_required
def like(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                liked_id = data.get('liked_id')
                liked_user = User.objects.get(id=liked_id)

                like = Like.objects.create(liker=request.user, liked=liked_user)

                mutual_like = Like.objects.filter(liker=liked_user, liked=request.user).exists()
                if mutual_like:
                    Match.objects.create(user1=request.user, user2=liked_user)
                    return JsonResponse({'success': True, 'message': 'It\'s a match!'})

                return JsonResponse({'success': True, 'message': 'Profile liked!'})

            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
     return JsonResponse({'success': False, 'message': 'Invalid request method.'})
'''
@login_required
def dislike(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'dislike':
                print("User disliked the profile!")
                return JsonResponse({'success': True, 'message': 'Profile disliked!'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid action!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
'''
@login_required
def matches(request):
    user_matches = Match.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    matched_users = [
        {
            'username': match.user2.username if match.user1 == request.user else match.user1.username,
            'age': match.user2.profile.age if match.user1 == request.user else match.user1.profile.age,
        }
        for match in user_matches
    ]
    return render(request, 'base/home.html', {'matches': matched_users})
'''

@login_required
def message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'message':
                print("User sent a message!")
                return JsonResponse({'success': True, 'message': 'Message sent!'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid action!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        age = request.POST.get('age', '')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'base/registration.html')   
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return render(request, 'base/registration.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            profile = Profile.objects.create(user=user, age=age)

            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            
            profile.save()

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {e}')
            return render(request, 'base/registration.html')

    return render(request, 'base/registration.html')

def check_username(request):
            if request.method == 'POST':
                data = json.loads(request.body)
                username = data.get('username', '')
                exists = User.objects.filter(username=username).exists()
                return JsonResponse({'exists': exists})
            return JsonResponse({'exists': False})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'base/login.html')

def profile(request):
    
    context = {
        'user' : request.user,
        'csrf-token' : request.COOKIES.get('csrftoken')
    }
    return render(request, 'base/profile.html', {'user': request.user})

@login_required
def chat_room(request):
    
    return render(request, 'chat_room.html', {
        'username': request.user.username,
    })

@login_required
def upload_photos(request):
    
    if request.method == 'POST' and request.FILES.getlist('profilePhotos'):
        uploaded_photos = []
        for file in request.FILES.getlist('profilePhotos'):
            photo = AdditionalPhoto.objects.create(user=request.user, profilePhotos=file)
            uploaded_photos.append({'url': photo.profilePhotos.url})
        return JsonResponse({'success': True, 'profilePhotos': uploaded_photos})
    return JsonResponse({'success': False})


def profileLogout(request):
    
    logout(request)
    
    return redirect('home')