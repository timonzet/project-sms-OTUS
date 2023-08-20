
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class ProfileUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(
        null=False, default=0, max_digits=30, decimal_places=2
    )
    phone = models.CharField(max_length=30, help_text='Required.')
    bio = models.TextField(null=False, blank=True)
    profile_pic = models.ImageField(null=False, blank=True, upload_to="images/profile/")
    facebook = models.CharField(max_length=50, null=False, blank=True)
    twitter = models.CharField(max_length=50, null=False, blank=True)
    instagram = models.CharField(max_length=50, null=False, blank=True)
    telegramm = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return str(self.user)



