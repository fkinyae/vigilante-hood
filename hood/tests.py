from django.test import TestCase
from .models import Profile, NeighbourHood, Posts, Business
from django.contrib.auth.models import User


# Create your tests here.

class ProfileTestClass(TestCase):
    from django.contrib.auth.models import User
    def setUp(self):
        self.user = User(username='martin')
        self.user.save()
        self.profile = Profile(id=1,user=self.user,profile_pic='download.jpeg',bio='My name is Martin', location='Ndarugo', hood_name='person')
        self.profile.save_user_profile()
    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        NeighbourHood.objects.all().delete()
    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
        self.assertTrue(isinstance(self.profile, Profile))
    def test_save_method(self):
        self.profile.save_user_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile) > 0)