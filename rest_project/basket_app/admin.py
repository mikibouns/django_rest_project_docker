from django.contrib import admin
from .models import Basket, ProductList


class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id')


class ProductListAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'product', 'quantity')


admin.site.register(Basket, BasketAdmin)
admin.site.register(ProductList, ProductListAdmin)