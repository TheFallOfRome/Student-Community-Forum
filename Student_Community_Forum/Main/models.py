from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    id_user = models.IntegerField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_images/', default='blank_profile_picture.jpg', null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return self.user.username