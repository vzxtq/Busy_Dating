import json
from django.http import JsonResponse
from .models import Profile
from .models import User
from .models import Message, AdditionalPhoto

def load_profiles(request):
    if request.method == 'GET':
        last_id = int(request.GET.get('last_id', 0))
        profiles = Profile.objects.filter(id__gt=last_id).exclude(user=request.user)[:10]
        
        user_profile = request.user.profile
        user_gender = user_profile.gender
        
        opposite_gender = 'F' if user_gender == 'M' else 'M'
        
        profiles= Profile.objects.filter(
            id__gt=last_id,
            gender=opposite_gender
        ).exclude(user=request.user)[:10]
        profiles_data = [
            {
                'id': profile.id,
                'username': profile.user.username,
                'photo': profile.photo.url,
                'age': profile.age,
                'bio': profile.bio,
                'gender': profile.gender,
            }
            for profile in profiles
        ]
        
        return JsonResponse({'profiles': profiles_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def load_messages(request):
    if request.method == 'GET':
        last_id = int(request.GET.get('last_id', 0))
        messages = Message.objects.filter(id__gt=last_id).order_by('timestamp')[:50]
        messages_data = [
            {
                'id': message.id,
                'sender': message.sender.username,
                'message': message.message,
                'timestamp': message.timestamp,
            }
            for message in messages
        ]
        return JsonResponse({'messages': messages_data})