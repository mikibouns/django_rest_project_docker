from django.contrib import admin
from .models import Products


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'art', 'price', 'quantity')


admin.site.register(Products, ProductsAdmin)
