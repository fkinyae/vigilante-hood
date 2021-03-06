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
        
        
class NeighbourHood(models.Model):
    name=models.CharField(max_length=200, blank=True)   
    locality = models.CharField(max_length=200, blank=True)
    occupants_count = models.IntegerField(null=True, blank=True)
    admin = models.ForeignKey('Profile',on_delete=models.CASCADE, related_name='hood')     
    hood_pic = models.ImageField(upload_to = 'hoods/profiles/', default='default.png')
    police_call = models.IntegerField(null=True, blank=True)
    hospital_call = models.IntegerField(null=True, blank=True)
    Fire_call = models.IntegerField(null=True, blank=True)
    
    
    def __str__(self):
        return str(self.name)
    
    def create_neighborhood(self):
        self.save()
        
    def delete_neigborhood(self):
        self.delete()
        
    @classmethod
    def find_neighborhood(cls, search_term):
        return cls.objects.filter(name__icontains=search_term)
    
    
    
class Business(models.Model):
    name = models.CharField(max_length=200,blank=True)
    brief = models.TextField(max_length=500, blank=True)
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)
    hood = models.ForeignKey('NeighbourHood', on_delete=models.CASCADE)
    emails = models.EmailField(max_length=200)
    
    def __str__(self):
        return str(self.name)
    
    def create_business(self):
        self.save()
        
    def delete_business(self):
        self.delete()
        
    @classmethod
    def update_business(cls, id):
        return cls.objects.update(id)
        
    @classmethod
    def find_business(cls, search_term):
        return cls.objects.filter(name__icontains=search_term).all()
    
    
    
class Posts(models.Model):
    alerts = (
        ("insecurity", "insecurity"),
        ("death", "death"),
        ("advertisement", "advertisement"),
        ("fundraising", "fundraising"),
        ("general information", "general information"),
        ("wedding/pre-wedding", "wedding/pre-wedding"),
        ("hood personnel", "hood personnel")
        )    
    type = models.CharField(choices = alerts, blank=True, max_length=200)
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True)
    hood = models.ForeignKey('NeighbourHood', on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.type)
    
    def save_post(self):
        self.save()
        
    def delete_post(self):
        self.delete()    
   
            
    

    
