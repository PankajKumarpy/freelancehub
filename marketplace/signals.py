from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import FreelancerProfile, ClientProfile, Review, Order
from django.utils import timezone
from decimal import Decimal


@receiver(post_save, sender=Review)
def update_freelancer_rating(sender, instance, created, **kwargs):
    """Update freelancer rating when a review is created"""
    if created:
        freelancer_profile = FreelancerProfile.objects.filter(user=instance.order.freelancer).first()
        if freelancer_profile:
            freelancer_profile.update_rating()


@receiver(post_save, sender=Order)
def update_freelancer_earnings(sender, instance, created, **kwargs):
    """Update freelancer earnings when order is completed"""
    if instance.status == 'Completed' and instance.completed_at:
        freelancer_profile = FreelancerProfile.objects.filter(user=instance.freelancer).first()
        if freelancer_profile:
            # Ensure price is Decimal type
            freelancer_profile.total_earnings += Decimal(str(instance.price))
            freelancer_profile.save()
