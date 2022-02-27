from django.contrib import admin
from billing.models import Bill, BillProducts 
# Register your models here.


class ProductsInline(admin.TabularInline):

    model = BillProducts
    fields = [
        'product', 
        'price', 
        'quantity'
    ]
    readonly_fields = [
        'product', 
        'price', 
        'quantity'
    ]
    extra = 0
    can_delete = False

    def has_add_permission(self, *args, **kwargs):
        return False

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):

    list_display = [
        'number', 
        "total_price", 
        'discount', 
        "end_price", 
        "bill_for", 
        "products", 
        "created_at", 
        "canceled_at"
    ] 

    inlines = [
        ProductsInline,
    ]

    
    def bill_for(self, obj):
        return obj.account.fullname

    def products(self, obj):
        return obj.bill_products.count()

    def end_price(self, obj):
        return abs(int(obj.discount - obj.total_price))