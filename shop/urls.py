from django.urls import path

from . import views


urlpatterns = [
    path("v1/product-list/<int:category_id>/", views.ProductListView.as_view(), name="product_list"),
    path("v1/product-detail/<str:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("v1/category-list/", views.CategoryListView.as_view(), name="category_list"),
    path("v1/cart/", views.CartDetailView.as_view(), name="cart_detail"),
    path("v1/cart-products/", views.CartProductListView.as_view(), name="cart_products"),
    path("v1/order/", views.OrderDetailView.as_view(), name="order_detail"),
    path("v1/delete-product-from-cart/", views.DeleteProductFromCartView.as_view(), name="delete_product_from_cart"),
    path("v1/change-qty-products/", views.ChangeQTYView.as_view(), name="change_qty_products"),
    path("v1/add-to-cart/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("v1/create-customer/", views.CreateCustomerView.as_view(), name="create_customer"),
    path("v1/get-customer/", views.GetCustomerView.as_view(), name="get_customer"),
    path("v1/create-order/", views.CreateOrderView.as_view(), name="create_order"),
    path("v1/lang/", views.GetCustomerLangView.as_view(), name="lang"),
    path("v1/change-lang/", views.ChangeCustomerLangView.as_view(), name="change_lang"),
]
