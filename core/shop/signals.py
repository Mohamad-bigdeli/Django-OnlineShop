from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product

@receiver(pre_save, sender=Product)
def calculate_discount_price(sender, instance, **kwargs):
    instance.discount_price = instance.price - instance.off
    