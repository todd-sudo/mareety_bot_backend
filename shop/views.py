import datetime

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from shop.models import (
    Cart, Order, CartProduct, Category, Product, Customer
)
from shop.utils import recalc_cart
from shop.serializers import (
    CategoryListSerializer,
    ProductSerializer,
    CartDetailSerializer,
    OrderDetailSerializer,
    RequestCartSerializer,
    RequestCreateCustomerSerializer,
    RequestGetCustomerSerializer,
    RequestChangeQTYSerializer, CartProductSerializer,
)


class CustomPageNumberPagination(PageNumberPagination):
    """ Кастомная пагинация
    """
    page_size = 5
    max_page_size = 20


class ProductListView(ListAPIView):
    """ Получение товаров
    """
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    queryset = Product.objects.all()
    lookup_field = "category_id"
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category")
        return queryset


class ProductDetailView(RetrieveAPIView):
    """ Получение товара
    """
    queryset = Product.objects.all()
    lookup_field = "id"
    serializer_class = ProductSerializer


class CategoryListView(ListAPIView):
    """ Получение категорий
    """
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategoryListSerializer


class CreateCustomerView(APIView):
    """ Создание покупателя
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=RequestCreateCustomerSerializer
    )
    def post(self, request: Request):

        tg_user_id = request.data.get("tg_user_id")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        lang = request.data.get("lang")
        phone = request.data.get("phone")
        address = request.data.get("address")
        if tg_user_id is None or first_name is None or last_name is None \
                or phone is None or address is None:
            return Response(
                {"msg": "error"}, status=status.HTTP_400_BAD_REQUEST
            )
        customer, _ = Customer.objects.get_or_create(
            tg_user_id=tg_user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            lang=lang or "uz",
        )
        Cart.objects.get_or_create(customer=customer)
        return Response({"msg": "ok"}, status=status.HTTP_200_OK)


class GetCustomerView(APIView):
    """ Получение покупателя
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=RequestGetCustomerSerializer
    )
    def post(self, request: Request):
        tg_user_id = request.data.get("tg_user_id")

        if tg_user_id is None:
            return Response(
                {"msg": "tg_user_id is null"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(tg_user_id=tg_user_id)
        except ObjectDoesNotExist:
            return Response(
                {"msg": "not customer"}, status=status.HTTP_400_BAD_REQUEST
            )
        Cart.objects.get_or_create(customer=customer, is_order=False)
        return Response({"lang": customer.lang}, status=status.HTTP_200_OK)


class GetCustomerLangView(APIView):
    """ Получение языка покупателя
    """
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "tguserid",
                OpenApiTypes.STR,
                description="TG ID пользователя",
                required=True,
                location="header"
            ),
        ],
    )
    def get(self, request: Request):
        tg_user_id = self.request.META.get("HTTP_TGUSERID")

        if tg_user_id is None:
            return Response(
                {"msg": "tg_user_id is null"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(tg_user_id=tg_user_id)
        except ObjectDoesNotExist:
            return Response(
                {"msg": "not customer"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"lang": customer.lang}, status=status.HTTP_200_OK)


class ChangeCustomerLangView(APIView):
    """ Изменение языка покупателя
    """
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "tguserid",
                OpenApiTypes.STR,
                description="TG ID пользователя",
                required=True,
                location="header"
            ),
        ],
    )
    def post(self, request: Request):
        tg_user_id = self.request.META.get("HTTP_TGUSERID")
        lang = request.data.get("lang")

        if lang is None:
            return Response(
                {"msg": "lang is null"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if tg_user_id is None:
            return Response(
                {"msg": "tg_user_id is null"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if lang not in ["uz", "ru", "en"]:
            return Response(
                {"msg": "not int langs"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(tg_user_id=tg_user_id)
        except ObjectDoesNotExist:
            return Response(
                {"msg": "not customer"}, status=status.HTTP_400_BAD_REQUEST
            )
        customer.lang = lang
        customer.save()
        return Response({"lang": customer.lang}, status=status.HTTP_200_OK)


class CartProductListView(ListAPIView):
    """ Получение товаров с корзины
    """
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPageNumberPagination

    @extend_schema(
        request=RequestCartSerializer,
        parameters=[
            OpenApiParameter(
                "tguserid",
                OpenApiTypes.STR,
                description="TG ID пользователя",
                required=True,
                location="header"
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        tg_user_id = self.request.META.get("HTTP_TGUSERID")
        try:
            customer = Customer.objects.get(tg_user_id=tg_user_id)
        except Customer.DoesNotExist:
            return Response(
                {"msg": "error"}, status=status.HTTP_400_BAD_REQUEST
            )
        queryset = CartProduct.objects.select_related("product")\
            .select_related("customer").select_related("cart")\
            .filter(customer=customer).filter(cart__is_order=False)
        return queryset


class CartDetailView(RetrieveAPIView):
    """ Получение товаров с корзины
    """
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RequestCartSerializer,
        parameters=[
            OpenApiParameter(
                "tguserid",
                OpenApiTypes.STR,
                description="TG ID пользователя",
                required=True,
                location="header"
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return Cart.objects.prefetch_related("products")\
            .select_related("customer")

    def get_object(self):
        tg_user_id = self.request.META.get("HTTP_TGUSERID")
        try:
            customer = Customer.objects.get(tg_user_id=tg_user_id)
        except Customer.DoesNotExist:
            return Response(
                {"msg": "error"}, status=status.HTTP_400_BAD_REQUEST
            )
        obj, created = Cart.objects.get_or_create(
            customer=customer, is_order=False
        )
        recalc_cart(obj)
        return obj


class OrderDetailView(ListAPIView):
    """ Получение заказа
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=RequestCartSerializer,
        parameters=[
            OpenApiParameter(
                "tguserid",
                OpenApiTypes.STR,
                description="TG ID пользователя",
                required=True,
                location="header"
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        tg_user_id = self.request.META.get("HTTP_TGUSERID")
        customer = Customer.objects.get(tg_user_id=tg_user_id)
        objects = Order.objects.filter(customer=customer)\
            .select_related("customer")\
            .select_related("cart")
        return objects


class DeleteProductFromCartView(APIView):
    """ Удаление товара из корзины
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RequestCartSerializer,
        parameters=[
            OpenApiParameter(
                "cart_id",
                OpenApiTypes.INT,
                description="ID корзины",
                required=True,
                location="cookie"
            ),
        ],
    )
    def post(self, request: Request):
        product_slug = request.data.get('product_slug')
        cart_id = int(request.COOKIES.get("cart_id"))
        cart = Cart.objects.get(pk=cart_id)
        print(cart_id, product_slug)
        print(cart.is_order)
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            customer=cart.customer, cart=cart, product=product
        )
        cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(cart)
        return Response({"msg": "ok"}, status=status.HTTP_200_OK)


class ChangeQTYView(APIView):
    """ Изменение кол-ва товаров в корзине
    """

    permission_classes = (AllowAny,)

    @extend_schema(
        request=RequestChangeQTYSerializer,
        parameters=[
            OpenApiParameter(
                "cart_id",
                OpenApiTypes.INT,
                description="ID корзины",
                required=True,
                location="cookie"
            ),
        ],
    )
    def post(self, request: Request):
        product_slug = request.data.get('product_slug')
        cart_id = int(request.COOKIES.get("cart_id"))
        cart = Cart.objects.get(pk=cart_id)
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            customer=cart.customer, cart=cart, product=product
        )
        qty = int(request.data.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(cart)
        return Response({"msg": "ok"}, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    """ Добавление товара в корзину
    """

    permission_classes = (AllowAny,)

    @extend_schema(
        request=RequestCartSerializer,
        parameters=[
            OpenApiParameter(
                "cart_id",
                OpenApiTypes.INT,
                description="ID корзины",
                required=True,
                location="cookie"
            ),
        ],
    )
    def post(self, request: Request):
        product_slug = request.data.get('product_slug')
        cart_id = int(request.COOKIES.get("cart_id"))
        cart = Cart.objects.get(pk=cart_id)
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            customer=cart.customer, cart=cart, product=product
        )
        if created:
            cart.products.add(cart_product)
        recalc_cart(cart)
        return Response({"msg": "ok"}, status=status.HTTP_201_CREATED)


class CreateOrderView(APIView):

    permission_classes = (AllowAny,)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                "cart_id",
                OpenApiTypes.INT,
                description="ID корзины",
                required=True,
                location="cookie"
            ),
        ],
    )
    def post(self, request: Request):
        cart_id = int(request.COOKIES.get("cart_id"))
        address = request.data.get("address")

        cart = Cart.objects.get(pk=cart_id)
        order = Order.objects.create(
            customer=cart.customer,
            cart=cart,
            address=address,
            created_at=datetime.date.today()
        )
        cart.is_order = True
        cart.save()
        serializer = OrderDetailSerializer(order, required=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

