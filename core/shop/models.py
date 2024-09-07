from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

class ProductFeature(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} : {self.value}"
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(max_length=1200)
    inventory = models.PositiveIntegerField(default=0)
    price= models.PositiveIntegerField(default=0)
    off = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0)
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, related_name="products_feature")
    

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=('id', 'slug')),
            models.Index(fields=['-created']),
            models.Index(fields=['name'])
        ]
    
    def __str__(self):
        return self.name



class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(upload_to='products_image/%Y%m%d')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
    
    def __str__(self):
        return self.product.name
