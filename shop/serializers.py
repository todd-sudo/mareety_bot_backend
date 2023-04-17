from rest_framework import serializers

from . import models


class RequestCartSerializer(serializers.Serializer):
    product_slug = serializers.CharField(max_length=1000, required=True)


class RequestChangeQTYSerializer(serializers.Serializer):
    product_slug = serializers.CharField(max_length=1000, required=True)
    qty = serializers.IntegerField(required=True)


class RequestCreateCustomerSerializer(serializers.Serializer):
    tg_user_id = serializers.CharField(required=True, max_length=60)
    first_name = serializers.CharField(required=True, max_length=300)
    last_name = serializers.CharField(required=True, max_length=300)
    phone = serializers.CharField(required=True, max_length=30)
    address = serializers.CharField(required=True, max_length=1000)


class RequestGetCustomerSerializer(serializers.Serializer):
    tg_user_id = serializers.CharField(required=True, max_length=60)


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(required=True)

    class Meta:
        model = models.Product
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = "__all__"


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = models.CartProduct
        exclude = ["customer", "cart"]


class CartDetailSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Cart
        exclude = ["customer"]


class CartOrderSerializer(serializers.ModelSerializer):

    products = CartProductSerializer(many=True)

    class Meta:
        model = models.Cart
        exclude = ["customer"]


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    cart = CartOrderSerializer(read_only=True)

    class Meta:
        model = models.Order
        fields = "__all__"
