from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Tự động tạo profile khi tạo user mới"""
    if created:
        try:
            UserProfile.objects.get_or_create(user=instance, defaults={'role': 'customer'})
        except:
            pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Lưu profile khi lưu user"""
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except:
        pass


