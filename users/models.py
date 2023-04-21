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

    @property
    def is_seller(self):
        return self.user_type == 'seller'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True)

class UserDocumentation(models.Model):

    DOCUMENT_TYPE_CHOICES = (
        ('DNI', 'DNI'),
        ('passport', 'passport'),
        ('driver license', 'driver license')
    )

    STATUS_CHOICES = (
        ('not uploaded', 'not uploaded'),
        ('uploaded', 'uploaded'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='documentation')

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, blank=True, null=True)
    document_identifier = models.CharField(max_length=30, blank=True, null=True)
    front_image = models.ImageField(upload_to='document_front', blank=True, null=True)
    back_image = models.ImageField(upload_to='document_back', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not uploaded')
    rejection_reason = models.TextField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=instance)
        if instance.is_superuser:
            EmailAddress.objects.create(user=instance, email=instance.email, verified=True, primary=True)