from django.contrib import admin
from account.models  import Account, Type
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = [
        'fullname', 
        "type", 
        "phone", 
        "address", 
        "balance"
    ] 
    readonly_fields = ['balance']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):

    list_display = [
        'name', 
        "count"
    ] 

    def count(self, obj):
        return obj.accounts.count()