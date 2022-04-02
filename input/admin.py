from django.contrib import admin

from .models import InputCategory, InputInventory, InputInventoryItem, InputProduct

# Register your models here.


admin.site.register(InputCategory)
admin.site.register(InputProduct)
admin.site.register(InputInventory)
admin.site.register(InputInventoryItem)
