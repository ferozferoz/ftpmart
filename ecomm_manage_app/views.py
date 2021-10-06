from django.contrib.auth.views import redirect_to_login
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .forms import *
from user_management_app.views import LoginView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Item,Category
from ecomm_app.models import Order, Delivery


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(Q(name='inventory') | Q(name='delivery')).exists():
            pass
        else:
            return redirect("/manager-login/")
        return super().dispatch(request, *args, **kwargs)


class ManagerLoginView(AdminRequiredMixin,LoginView):
    success_url = reverse_lazy("ecomm_manage_app:manager_home")


class ManagerHomeView(AdminRequiredMixin, TemplateView):
    template_name = "ecomm_manage_app/manager_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_orders"] = Order.objects.all().order_by("-id")
        return context


"""
permission mixin will be used to provide access to list, update and create view
for users where the resource do not have permission, it should go back to the previous page

"""

class UserAccessMixin(PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(),reverse_lazy("ecomm_manage_app:manager_login"),self.get_redirect_field_name())
        if not self.has_permission():
            return redirect_to_login(self.request.get_full_path(),reverse_lazy("ecomm_manage_app:manager_login"),self.get_redirect_field_name())
        return super(UserAccessMixin,self).dispatch(request,*args,**kwargs)


class ProductListView(UserAccessMixin, ListView):

    template_name = "ecomm_manage_app/product_list.html"
    queryset = Item.objects.all().order_by("-id")
    context_object_name = "all_products"
    permission_required = 'ecomm_manage_app.view_item'
    raise_exception = True
    permission_denied_message = "You dont have permissions to access the page"


class CategoryListView(UserAccessMixin, ListView):

    template_name = "ecomm_manage_app/category_list.html"
    queryset = Category.objects.all().order_by("-id")
    context_object_name = "all_categories"
    permission_required = 'ecomm_manage_app.view_category'


class ProductUpdateView(UserAccessMixin, UpdateView):
    template_name = "ecomm_manage_app/product_create.html"
    form_class = ProductForm
    # we need to implement this variable as  part of List View ,rest ListView object handles
    queryset = Item.objects.all()
    success_url = reverse_lazy("ecomm_manage_app:product_list")
    permission_required = 'ecomm_manage_app.change_item'

    def get_object(self):
        id_ = self.kwargs.get("slug")
        return get_object_or_404(Item, slug=id_)

    def form_valid(self, form):
        product_name = form.cleaned_data.get("name")
        p = form.save()
        return super().form_valid(form)


class ProductCreateView(UserAccessMixin, CreateView):
    template_name = "ecomm_manage_app/product_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomm_manage_app:product_list")
    permission_required = 'ecomm_manage_app.add_item'

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")

        return super().form_valid(form)


class CategoryCreateView(UserAccessMixin, CreateView):
    template_name = "ecomm_manage_app/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("ecomm_manage_app:category_list")
    permission_required = 'ecomm_manage_app.add_category'

    def form_valid(self, form):
        p = form.save()
        return super().form_valid(form)


class CategoryUpdateView(UserAccessMixin, UpdateView):
    template_name = "ecomm_manage_app/category_create.html"
    form_class = CategoryForm
    # we need to implement this variable as  part of List View ,rest ListView object handles
    queryset = Category.objects.all()
    success_url = reverse_lazy("ecomm_manage_app:category_list")
    permission_required = 'ecomm_manage_app.change_supplier'

    def get_object(self):
        id_ = self.kwargs.get("slug")
        return get_object_or_404(Category, slug=id_)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SupplierListView(UserAccessMixin, ListView):
    template_name = "ecomm_manage_app/supplier_list.html"
    queryset = Supplier.objects.all().order_by("-id")
    context_object_name = "all_suppliers"
    permission_required = 'ecomm_manage_app.view_supplier'


class SupplierUpdateView(UserAccessMixin, UpdateView):
    template_name = "ecomm_manage_app/supplier_create.html"
    form_class = SupplierForm
    # we need to implement this variable as  part of List View ,rest ListView object handles
    queryset = Supplier.objects.all()
    success_url = reverse_lazy("ecomm_manage_app:supplier_list")
    permission_required = 'ecomm_manage_app.change_supplier'

    def get_object(self):
        id_ = self.kwargs.get("slug")
        return get_object_or_404(Supplier, slug=id_)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SupplierCreateView(UserAccessMixin, CreateView):
    template_name = "ecomm_manage_app/supplier_create.html"
    form_class = SupplierForm
    success_url = reverse_lazy("ecomm_manage_app:supplier_list")
    permission_required = 'ecomm_manage_app.add_supplier'

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)


class WarrantyCreateView(UserAccessMixin, CreateView):
    template_name = "ecomm_manage_app/warranty_create.html"
    form_class = WarrantyForm
    success_url = reverse_lazy("ecomm_manage_app:warranty_list")
    permission_required = 'ecomm_manage_app.add_supplier'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class WarrantyUpdateView(UserAccessMixin, UpdateView):

    template_name = "ecomm_manage_app/warranty_create.html"
    form_class = WarrantyForm
    # we need to implement this variable as  part of List View ,rest ListView object handles
    queryset = Warranty.objects.all()
    success_url = reverse_lazy("ecomm_manage_app:warranty_list")
    permission_required = 'ecomm_manage_app.change_category'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Warranty, id=id_)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class WarrantyListView(UserAccessMixin, ListView):
    template_name = "ecomm_manage_app/warranty_list.html"
    queryset = Warranty.objects.all().order_by("-id")
    context_object_name = "all_warranty"
    permission_required = 'ecomm_manage_app.view_supplier'


class ReturnPolicyCreateView(UserAccessMixin, CreateView):
    template_name = "ecomm_manage_app/return_policy_create.html"
    form_class = ReturnPolicyForm
    success_url = reverse_lazy("ecomm_manage_app:return_policy_list")
    permission_required = 'ecomm_manage_app.add_supplier'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ReturnPolicyUpdateView(UserAccessMixin, UpdateView):

    template_name = "ecomm_manage_app/return_policy_create.html"
    form_class = ReturnPolicyForm
    # we need to implement this variable as  part of List View ,rest ListView object handles
    queryset = ReturnPolicy.objects.all()
    success_url = reverse_lazy("ecomm_manage_app:return_policy_list")
    permission_required = 'ecomm_manage_app.change_category'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ReturnPolicy, id=id_)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ReturnPolicyListView(UserAccessMixin, ListView):
    template_name = "ecomm_manage_app/return_policy_list.html"
    queryset = ReturnPolicy.objects.all().order_by("-id")
    context_object_name = "all_return_policy"
    permission_required = 'ecomm_manage_app.view_supplier'


class OpenOrdersListView(UserAccessMixin, ListView):
    template_name = "ecomm_manage_app/open_orders_list.html"
    queryset = Order.objects.filter(~(Q(order_status= 'OPEN')))
    context_object_name = "open_orders"
    permission_required = 'ecomm_manage_app.view_supplier'


class OrderDeliveryDetailView(UserAccessMixin, TemplateView):

    template_name = "ecomm_manage_app/order_delivery_details.html"
    permission_required = 'ecomm_manage_app.view_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        context["order_obj"] = order_obj
        context["cart"] = order_obj.cart
        return context


class OrderDeliveryUpdateView(UserAccessMixin, View):

    template_name = "ecomm_manage_app/order_delivery_details.html"
    permission_required = 'ecomm_manage_app.view_supplier'

    def get(self, request, *args, **kwargs):
        context = {}

        delivery_status = request.GET['delivery']
        order_id = self.kwargs["pk"]
        order = get_object_or_404(Order, pk=order_id)
        context["order_obj"] = order
        context["cart"] = order.cart

        Delivery.objects.create(order=order,
                                delivery_status=delivery_status,
                                delivery_manager=request.user)

        if delivery_status == 'DELIVERED':
            order.order_status = 'COMPLETE'
            order.save()

        return render(request, self.template_name, context)



def get_order_status(request):
    order_id = request.GET.get('order_id', None)
    order = Order.objects.get(pk = order_id)
    return JsonResponse({"order_status": order.order_status})


