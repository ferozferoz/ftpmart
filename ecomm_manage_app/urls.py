
from django.urls import path
from .views import *
from user_management_app.views import *

app_name= "ecomm_manage_app"

urlpatterns = [

        path("manager-login/", ManagerLoginView.as_view(), name="manager_login"),
        path("manager-home/", ManagerHomeView.as_view(), name="manager_home"),
        path("manage-order-details/<int:pk>/", OrderDeliveryDetailView.as_view(), name="order_delivery_details"),
        path("manage-order-details/<int:pk>/update", OrderDeliveryUpdateView.as_view(), name="order_delivery_update"),
        path("manage-open-orders/", OpenOrdersListView.as_view(), name="open_order_list"),
        path("get_order_status/", get_order_status, name="get_order_status"),
        path("manage-product/list/", ProductListView.as_view(), name="product_list"),
        path("manage-product/add/", ProductCreateView.as_view(), name="product_create"),
        path("manage-product/<slug:slug>/update/", ProductUpdateView.as_view(), name="product_update"),
        path("manage-category/list/", CategoryListView.as_view(), name="category_list"),
        path("manage-category/add/", CategoryCreateView.as_view(), name="category_create"),
        path("manage-category/<slug:slug>/update/", CategoryUpdateView.as_view(), name="category_update"),
        path("manage-supplier/list/", SupplierListView.as_view(), name="supplier_list"),
        path("manage-supplier/add/", SupplierCreateView.as_view(), name="supplier_create"),
        path("manage-supplier/<slug:slug>/update/", SupplierUpdateView.as_view(), name="supplier_update"),
        path("manage-warranty/list/", WarrantyListView.as_view(), name="warranty_list"),
        path("manage-warranty/add/", WarrantyCreateView.as_view(), name="warranty_create"),
        path("manage-warranty/<int:pk>/update/", WarrantyUpdateView.as_view(), name="warranty_update"),
        path("manage-return_policy/list/", ReturnPolicyListView.as_view(), name="return_policy_list"),
        path("manage-return-policy/add/", ReturnPolicyCreateView.as_view(), name="return_policy_create"),
        path("manage-return-policy/<int:pk>/update/", ReturnPolicyUpdateView.as_view(), name="return_policy_update"),

]