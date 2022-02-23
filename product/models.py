from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
user_model = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=45, unique=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):

        return self.name 

class Product(models.Model):
    """Product Model"""
    name = models.CharField(max_length=255)
    selling_price = models.IntegerField()
    purchasing_price = models.IntegerField()
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Create by 
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="products")

    # gategory product
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", blank=True, null=True)


    def __str__(self):

        return self.name 

