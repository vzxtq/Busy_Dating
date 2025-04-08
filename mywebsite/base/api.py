import json
from .models import User
from .models import Message, AdditionalPhoto
from django.http import JsonResponse
from .models import Profile

def load_profiles(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    last_id = int(request.GET.get('last_id', 0))
    
    user_profile = getattr(request.user, 'profile', None)
    user_gender = getattr(user_profile, 'gender', None)

    if not user_gender:
        profiles = Profile.objects.filter(id__gt=last_id).exclude(user=request.user)[:10]
    else:
        opposite_gender = 'F' if user_gender == 'M' else 'M'

        profiles = Profile.objects.filter(
            id__gt=last_id,
            gender=opposite_gender
        ).exclude(user=request.user)[:10]

    profiles_data = [
        {
            'id': profile.id,
            'username': profile.user.username,
            'photo': profile.photo.url if profile.photo else '/media/default.jpg',
            'age': profile.age,
            'bio': profile.bio,
            'gender': profile.gender,
        }
        for profile in profiles
    ]

    return JsonResponse({'profiles': profiles_data})


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
    return JsonResponse({'error': 'Invalid request method'}, status=405)