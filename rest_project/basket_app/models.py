from django.db import models
from product_app.models import Products
from django.contrib.auth import get_user_model

User = get_user_model()


class Basket(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')

    def __str__(self):
        return str('Basket: {}, User: {}'.format(self.id, self.user_id))

    def product_children(self):
        return ProductList.objects.filter(basket=self)


class ProductList(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='prod')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product.name)

    @staticmethod
    def quantity_calculation(product, quantity):
        if quantity > 0:
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()
                return True
            else:
                return False
        elif quantity < 0:
            product.quantity += abs(quantity)
            product.save()
            return True
        else:
            return False
