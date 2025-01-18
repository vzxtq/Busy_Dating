from django.urls import path
from . import views
from . import api
from .views import delete_selected_photos
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('api/load_profiles/', api.load_profiles, name='load_profiles'),
    path('send/', views.send_message, name='send_message'),
    path('api/load_messages/', api.load_messages, name='load_messages'),
    path('registration/', views.signup, name = 'registration'),
    path('check_username/', views.check_username, name='check_username'),
    path('login/', views.login, name='login'),
    path('registration/login', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('upload_photos/', views.upload_photos, name='upload_photos'),
    path('logout/', views.profileLogout, name='logout'),
    path('delete_selected_photos/', delete_selected_photos, name='delete_selected_photos'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)