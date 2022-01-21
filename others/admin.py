from django.contrib import admin
from others.models  import Other, Type
# Register your models here.

@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):

    list_display = ['fullname', "type", "phone", "address"] 


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):

    list_display = ['name', "count"] 

    def count(self, obj):
        return obj.others.count()