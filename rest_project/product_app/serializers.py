from .models import Products
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
)


class ProductsSerializer(ModelSerializer):

    class Meta:
        model = Products
        fields = ('art', 'name', 'price', 'quantity')


class ProductsUpdateSerializer(ModelSerializer):
    art = CharField(read_only=True)

    class Meta:
        model = Products
        fields = ('art', 'name', 'price', 'quantity')