from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user_model = get_user_model()


class Debt(models.Model):
    """Debt model"""
    price = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    account = models.ForeignKey("account.Account", on_delete=models.CASCADE, related_name="debts")
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="debts")

    __format_date = '%Y-%m-%d'

    @property
    def created_date(self):
        return self.created_at.strftime(self.__format_date)

    @property
    def updated_date(self):
        if self.updated_at:
            return self.updated_at.strftime(self.__format_date)
        return "---"