from django.db import models
from django.contrib.auth import get_user_model
from datetime import date 

user_model = get_user_model()

# Create your models here.
class Bill(models.Model):
    """Billing Model"""

    __format_date = '%Y-%m-%d'


    number = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True)

    account = models.ForeignKey("account.Account", on_delete=models.CASCADE, related_name="billing")
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="billing")

    @property
    def price(self):
        return self.total_price
    
    @property
    def created_date(self):
        return self.created_at.strftime(self.__format_date)

    @property
    def canceled_date(self):
        if self.canceled_at:
            return self.canceled_at.strftime(self.__format_date)
        return "---"


class BillProducts(models.Model):
    """Products for bill"""

    price = models.IntegerField()
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="product_billing")
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="bill_products")


    