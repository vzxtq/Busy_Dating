from django.urls import path
from . import views
from . import api
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('api/load_profiles/', api.load_profiles, name='load_profiles'),
    #path('api/like/', api.like_profile, name='like_profile'),
    #path('matches/', views.matches, name='matches'),
    path('dislike/', views.dislike, name = 'dislike'),
    path('message/', views.message, name = 'message'),
    path('registration/', views.signup, name = 'registration'),
    path('check_username/', views.check_username, name='check_username'),
    path('login/', views.login, name='login'),
    path('registration/login', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('upload_photos/', views.upload_photos, name='upload_photos'),
    path('logout/', views.profileLogout, name='logout'), 
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)