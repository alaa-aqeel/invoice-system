from django.contrib import admin
from product.models import Product, Category
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', "selling_price", "purchasing_price", "category", "quantity"] 


class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name', "selling_price", "purchasing_price", 'quantity', 'user']
    readonly_fields = ["name", "selling_price", "purchasing_price", 'quantity', 'user']
    extra = 0
    can_delete = False


    def has_add_permission(self, *args, **kwargs):
        return False

@admin.register(Category)
class CategroyAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]

    list_display = ['name', "products"] 

    def products(self, obj):
        return obj.products.count()