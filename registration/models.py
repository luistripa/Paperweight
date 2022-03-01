from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProtectionLevels:
    PUBLIC = 1  # All logged in users
    RESTRICTED = 2  # All staff users
    TOP_SECRET = 3  # Only the creator and superusers
    ULTRA_TOP_SECRET = 4
    CHOICES = (
        (PUBLIC, 'Public'),
        (RESTRICTED, 'Restricted'),
        (TOP_SECRET, 'Top Secret'),
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permissions = models.IntegerField(choices=ProtectionLevels.CHOICES, default=ProtectionLevels.PUBLIC)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created, **kwargs):
    if created:
        if instance.is_superuser:
            Profile.objects.create(user=instance, permissions=ProtectionLevels.TOP_SECRET)
        elif instance.is_staff:
            Profile.objects.create(user=instance, permissions=ProtectionLevels.RESTRICTED)
        else:
            Profile.objects.create(user=instance)  # default PUBLIC


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs):
    instance.profile.save()
