from django.contrib import admin
from debts.models import Debt
# Register your models here.

@admin.register(Debt)
class DebtsAdmin(admin.ModelAdmin):

    list_display = [
        "id", 
        "account", 
        'price', 
        "user",
        'created_at',
        'updated_at',
        'deleted_at',
    ] 


