# -*- coding: utf-8 -*-

from django.urls import path
from .views import *

app_name= "ecomm_app"

urlpatterns = [

        path("", HomeView.as_view(), name="home"),
        path("contact/", Contact.as_view(), name="contact_us"),
        path("all-category-products/<slug:slug>/", CategoryProductsView.as_view(), name="category_products"),
        path("all-subcategory-products/<slug:slug>/", SubCategoryProductsView.as_view(), name="sub_category_products"),
        path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
        path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="add_to_cart"),
        path("my-cart/", MyCartView.as_view(), name="my_cart"),
        path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="manage_cart"),
        path("check_out/", CheckoutView.as_view(), name="check_out"),
        path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customer_order_detail"),
        path("search/", SearchView.as_view(), name="search"),
        path("orderplace/", OrderPlacedView.as_view(), name="order_placed"),
        path("admin-login/", AdminLoginView.as_view(), name="admin_login"),
        path("admin-home/", AdminHomeView.as_view(), name="admin_home"),
        path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(), name="admin_order_detail"),
        path("admin-all-orders/", AdminOrderListView.as_view(), name="admin_order_list"),
        path("admin-order-<int:pk>-change/", AdminOrderStatuChangeView.as_view(), name="admin_order_status_change"),
        path("admin-product/list/", AdminProductListView.as_view(), name="admin_product_list"),
        path("admin-product/add/", AdminProductCreateView.as_view(), name="admin_product_create"),
        path("admin-product/<slug:slug>/update/", AdminProductUpdateView.as_view(), name="admin_product_update")

]