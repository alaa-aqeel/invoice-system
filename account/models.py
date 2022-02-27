from django.db import models
from django.db.models import Sum
# Create your models here.

class Type(models.Model):
    """Type for customer or supplier """
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class Account(models.Model):
    """Account Model"""
    fullname = models.CharField(max_length=45)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    # balance =  models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # type Customer or Supplier
    type = models.ForeignKey(Type, on_delete=models.CASCADE, 
                            related_name="accounts")

    @property
    def debt(self):
        """Get total debts"""
        total_debts =  self.billing.filter(canceled_at=None).aggregate(Sum('total_price')).get("total_price__sum", 0)
        if total_debts:
            return total_debts
        return 0

    @property
    def paid(self):
        """Get total paid"""
        total_paid = self.debts.filter(deleted_at=None).aggregate(Sum('price')).get("price__sum", 0) 
        if total_paid:
            return total_paid
        return 0

    @property
    def balance(self):
        return self.debt - self.paid

    def __str__(self):
        return self.fullname
