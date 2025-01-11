from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
        
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
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

'''
class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_sent")
    liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_received")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.liker.username} liked {self.liked.username}"
          
class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_as_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_as_user2")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user1.username} matched with {self.user2.username}"
'''    