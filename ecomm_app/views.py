from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib import messages
from user_management_app.forms import CustomerLoginForm
from user_management_app.models import Customer


"""Mixin class that contain common cart objects"""


class ECommMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        print("method - EcommMixin, Cart id -" + str(cart_id))

        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            print("method - EcommMixin, customer - " + str(cart_obj))
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


"""Mixin class that contain common cart objects"""


class CartNo(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        context['categories'] = Category.objects.filter(parent=None)
        return context


"""Function return Main page"""


class HomeView(ECommMixin, CartNo, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_products'] = Item.objects.all()

        return context


class Contact(CartNo, ECommMixin, TemplateView):
    template_name = "contact.html"


class CategoryProductsView(CartNo, ECommMixin, TemplateView):
    template_name = "all_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        bread_crumb = category.__str__().split('->')

        list_objects = []
        for cat in bread_crumb:
            list_objects.append(Category.objects.get(name=cat))

        category_items = category.category.all()
        context['category_items'] = category_items
        context['category'] = category
        context['bread_crumb'] = list_objects

        return context


class SubCategoryProductsView(CartNo, ECommMixin, TemplateView):
    template_name = "all_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        bread_crumb = category.__str__().split('->')
        list_objects = []
        for cat in bread_crumb:
            list_objects.append(Category.objects.get(name=cat))

        category_items = category.sub_category.all()
        context['category_items'] = category_items
        context['category'] = category
        context['bread_crumb'] = list_objects
        return context


class ProductDetailView(CartNo, ECommMixin, TemplateView):
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Item.objects.get(slug=url_slug)
        similar_product = Item.objects.filter(category=product.category).exclude(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        context['sim_prod'] = similar_product
        return context


class AddToCartView(CartNo, ECommMixin, View):

    def get(self, request, *args, **kwargs):
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Item.objects.get(id=product_id)
        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cart_product = this_product_in_cart.last()
                cart_product.quantity += 1
                cart_product.subtotal += product_obj.display_new_selling_price
                cart_product.save()
                cart_obj.total += product_obj.display_new_selling_price
                cart_obj.save()
            # new item is added in cart
            else:
                cart_product = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.display_new_selling_price, quantity=1,
                    subtotal=product_obj.display_new_selling_price)
                cart_obj.total += product_obj.display_new_selling_price
                cart_obj.save()



        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cart_product = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.display_new_selling_price, quantity=1,
                subtotal=product_obj.display_new_selling_price)
            cart_obj.total += product_obj.display_new_selling_price
            cart_obj.save()
        messages.success(request, 'Product added to the cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class MyCartView(CartNo, ECommMixin, TemplateView):
    template_name = "my_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class ManageCartView(ECommMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("ecomm_app:my_cart")


class CheckoutView(ECommMixin, CreateView):
    template_name = "check_out.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomm_app:order_placed")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/check_out/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            Order.objects.update_or_create(cart = cart_obj,
                                 customer = cart_obj.customer,
                                 subtotal = cart_obj.total,
                                 discount = 0,
                                 total = cart_obj.total,
                                 order_status = 'Order Received')

            customer = Customer.objects.filter(user=cart_obj.customer.user)
            customer_details = form.cleaned_data
            customer.update(**customer_details)


            #subject = 'Order Placed'
            #message = f'Hi, thank you for placing an order.'
            #email_from = settings.EMAIL_HOST_USER
            #recipient_list = [form['email'].value(), ]
            #send_mail(subject, message, email_from, recipient_list)
            del self.request.session['cart_id']
        else:
            return redirect("ecomm_app:home")
        return redirect("ecomm_app:order_placed")


class OrderPlacedView(CartNo, TemplateView):
    template_name = "order_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        order = Order.objects.filter(customer=customer).order_by("-id")[0]
        # order_id=orders.id
        cart_products = CartProduct.objects.filter(cart=order.cart)
        context['cart_products'] = cart_products
        context['orders'] = order
        return context


ORDER_STATUS2 = (
    ("Order Cancelled", "Cancel Order"),
    ("Return Requested", "Request Return"),

)


class CustomerOrderDetailView(CartNo, DetailView):
    template_name = "customer_order_detail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("ecomm_app:customer_profile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS2
        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomm_app:customer_order_detail", kwargs={"pk": order_id}))


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(title__icontains=kw) | Q(description__icontains=kw) | Q(return_policy__icontains=kw))

        context["results"] = results
        return context


# aadmin

class AdminLoginView(FormView):
    template_name = "admin/admin_login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomm_app:admin_home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "admin/admin_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        return context


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "admin/admin_order_details.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context


class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "admin/admin_order_list.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"


class AdminOrderStatuChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        subject = "Update on your order "
        message = f'Hi {order_obj.ordered_by}, status of your changed to {new_status}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [order_obj.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect(reverse_lazy("ecomm_app:admin_order_detail", kwargs={"pk": order_id}))


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "admin/admin_product_list.html"
    queryset = Item.objects.all().order_by("-id")
    context_object_name = "allproducts"


class AdminProductUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admin/admin_product_create.html"
    form_class = ProductForm
    # we need to implement this variable as  part of List View ,rest ListView object handles
    queryset = Item.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("slug")
        return get_object_or_404(Item, slug=id_)

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "admin/admin_product_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomm_app:admin_product_list")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)
