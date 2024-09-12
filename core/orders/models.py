from django.db import models
from shop.models import Product

# Create your models here.

class Oreder(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight < 1000:
            return 10
        elif 1000 <= weight <= 2000:
            return 12.5
        else: 
            return 15

    def get_final_cost(self):
        price = self.get_post_cost() + self.get_total_cost()
        return price   

    def __str__(self):
        return f"order : {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Oreder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)
    
    def get_cost(self):
        return self.price * self.quantity
    
    def get_weight(self):
        return self.weight * self.quantity

    def __str__(self):
        return str(self.id)
    