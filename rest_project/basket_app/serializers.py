from .models import Basket, ProductList
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    CharField,
    ReadOnlyField
)


class ProductListSerializer(ModelSerializer):
    product = CharField(read_only=True)
    art = SerializerMethodField(read_only=True)

    class Meta:
        model = ProductList
        fields = ('id', 'product', 'art', 'quantity')

    def get_art(self, obj):
        return obj.product.art

    def create(self, validated_data):
        validated_data['basket'] = self.context.get('basket')
        print(validated_data)
        try:
            ProductList.objects.filter(basket=validated_data.get('basket')).get(product=validated_data.get('product'))
            raise ValidationError({'product': ['product {} already exists in the basket'.format(validated_data.get('product').art)]})
        except ProductList.DoesNotExist:
            if ProductList.quantity_calculation(product=validated_data.get('product'), quantity=abs(validated_data.get('quantity', 1))):
                purchase = ProductList.objects.create(**validated_data)
                return purchase
            raise ValidationError({'quantity': 'not enough products in stock, check product availability'})

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', None)
        if quantity:
            remain = quantity - instance.quantity
            instance.quantity = quantity
            if ProductList.quantity_calculation(product=instance.product, quantity=remain):
                instance.save()
                return instance
            raise ValidationError({'quantity': 'not enough products in stock, check product availability'})


class BasketSerializer(ModelSerializer):
    products = SerializerMethodField()
    basket_id = SerializerMethodField(read_only=True)

    class Meta:
        model = Basket
        fields = ('basket_id', 'user_id', 'products')

    def get_products(self, obj):
        data = ProductListSerializer(obj.product_children(), many=True).data
        if data:
            return data
        return None

    def get_basket_id(self, obj):
        return obj.id


class AddToBasketSerializer(ModelSerializer):
    product_name = SerializerMethodField(read_only=True)
    id = ReadOnlyField()

    class Meta:
        model = ProductList
        fields = ('id', 'product', 'product_name', 'quantity')

    def get_product_name(self, obj):
        return obj.product.name

    def create(self, validated_data):
        validated_data['basket'] = self.context.get('basket')
        try:
            ProductList.objects.filter(basket=validated_data.get('basket')).get(product=validated_data.get('product'))
            raise ValidationError({'product': ['product {} already exists in the basket'.format(validated_data.get('product').art)]})
        except ProductList.DoesNotExist:
            if ProductList.quantity_calculation(product=validated_data.get('product'), quantity=abs(validated_data.get('quantity', 1))):
                purchase = ProductList.objects.create(**validated_data)
                return purchase
            raise ValidationError({'quantity': 'not enough products in stock, check product availability'})
