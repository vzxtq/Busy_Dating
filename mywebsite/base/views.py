from django import forms
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
import json
from django.contrib.auth.decorators import login_required
from .models import AdditionalPhoto, Profile, Message
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import sync_to_async

def home(request):
    return render(request, 'base/home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        age = request.POST.get('age', '')
        bio = request.POST.get('bio','')
        gender = request.POST.get('gender', '')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'base/registration.html')   
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return render(request, 'base/registration.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            profile = Profile.objects.create(user=user, age=age, bio=bio, gender=gender)

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

@csrf_exempt
def profile(request): 
    context = {
        'user' : request.user,
        'csrf-token' : request.COOKIES.get('csrftoken')
    }
    profile_photos = AdditionalPhoto.objects.filter(user=request.user)

    return render(request, 'base/profile.html', {'user': request.user})

@login_required
def chat_room(request):
    messages = Message.objects.order_by('-timestamp')
    return render(request, 'chat_room.html', {
        'username': request.user.username,
    })
    
@sync_to_async    
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        text = request.POST.get('message', '')
        if text:
            message = Message.objects.create(sender=sender, text=text)
            return JsonResponse({'user': sender.username, 'text': message.text, 'timestamp': message.timestamp})
        else:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
def upload_photos(request):
    if request.method == 'POST':
        uploaded_photos = []
        for file in request.FILES.getlist('profilePhotos'):
            photo = AdditionalPhoto.objects.create(user=request.user, profilePhotos=file)
            uploaded_photos.append({'url': photo.profilePhotos.url})
        return JsonResponse({'success': True, 'profilePhotos': uploaded_photos})
    return JsonResponse({'success': False})


def profileLogout(request):
    logout(request)
    
    return redirect('home')


@csrf_exempt
@login_required
def delete_selected_photos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            photo_ids = data.get('photo_ids', [])
            
            photos = AdditionalPhoto.objects.filter(id__in=photo_ids, user=request.user)
            
            for photo in photos:
                photo.profilePhotos.delete()
                photo.delete()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
