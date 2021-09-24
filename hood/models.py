from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True,null=True)
    profile_pic = models.ImageField(upload_to='images/profile/', default='default.png')
    location = models.CharField(max_length=255, blank=True,null=True)
    hood_name = models.CharField(max_length=255, blank=True,null=True)
  
    def __str__(self):
        return str(self.user)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
