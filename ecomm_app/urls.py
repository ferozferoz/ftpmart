# -*- coding: utf-8 -*-

from django.urls import path
from .views import *
from user_management_app.views import *

app_name = "ecomm_app"

urlpatterns = [

        path("", HomeView.as_view(), name="home"),
        path("all-category-products/<slug:slug>/", CategoryProductsView.as_view(), name="category_products"),
        #path("all-subcategory-products/<slug:slug>/", SubCategoryProductsView.as_view(), name="sub_category_products"),
        path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
        path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="add_to_cart"),
        path("my-cart/", MyCartView.as_view(), name="my_cart"),
        path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="manage_cart"),
        path("check_out/", CheckoutView.as_view(), name="check_out"),
        path("order-detail/order-<int:pk>/", OrderDetailView.as_view(), name="order_details"),
        path("search/", SearchView.as_view(), name="search"),
        path("order_place/", OrderPlacedView.as_view(), name="order_placed"),
        path("manage-cart/", ShipOrderView.as_view(), name="ship_order"),
        path("cancel-order/order-<int:pk>/", CancelOrderView.as_view(), name="cancel_order"),
        path("profile/", CustomerProfileView.as_view(), name="customer_profile"),
        path("profile_edit", editCustomerProfileView, name="edit_customer_profile"),

]