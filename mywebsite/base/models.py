from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),    
        ('F', 'Female'),  
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=1000)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES) 
    
    def __str__(self):
        return f'{self.user.username} Profile'


class AdditionalPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profilePhotos = models.ImageField(upload_to='additional_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo {self.user.username}'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    message = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} : {self.message}"        
