from django.db import models


class Products(models.Model):
    art = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)