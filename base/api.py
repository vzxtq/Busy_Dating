import json
from django.http import JsonResponse
from .models import Profile
from .models import User

def load_profiles(request):
    if request.method == 'GET':
        last_id = int(request.GET.get('last_id', 0))
        profiles = Profile.objects.filter(id__gt=last_id).exclude(user=request.user)[:10]
        
        profiles_data = [
            {
                'id': profile.id,
                'username': profile.user.username,
                'photo': profile.photo.url,
                'age': profile.age,
            }
            for profile in profiles
        ]
        
        return JsonResponse({'profiles': profiles_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

'''
def like_profile(request):
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