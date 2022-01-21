from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()

# Create your models here.
class Bill(models.Model):
    """Billing Model"""
    code = models.CharField(max_length=255)
    total_price = models.IntegerField()
    discount = models.IntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    other = models.ForeignKey("others.Other", on_delete=models.CASCADE, related_name="billing")
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="billing")


class BillProducts(models.Model):
    """Products for bill"""

    price = models.IntegerField()
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="product_billing")
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="bill_products")


    