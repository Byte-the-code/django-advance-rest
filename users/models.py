from allauth.account.models import EmailAddress

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'buyer'),
        ('seller', 'seller'),
    )
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES, default='buyer')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True)

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=instance)
        if instance.is_superuser:
            EmailAddress.objects.create(user=instance, email=instance.email, verified=True, primary=True)
