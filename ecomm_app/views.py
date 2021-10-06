from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.utils.html import strip_tags

from .models import *
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib import messages
from user_management_app.views import *
from ecomm_manage_app.models import Category
from django.template.loader import render_to_string


"""Mixin class that contain common cart objects"""


class CartNo(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = get_object_or_404(NewCart, id=cart_id)
        else:
            cart = None

        context['cart'] = cart
        context['categories'] = Category.objects.all()
        context['category_nav'] = Category.objects.filter(parent_id=None)
        context['all_items'] = Item.objects.all()
        context['is_manager'] = self.request.user.groups.filter(Q(name='inventory') | Q(name='delivery')).exists()
        return context


"""Function return Main page"""


class HomeView( CartNo, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryProductsView(CartNo, TemplateView):
    template_name = "all_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        category = context['categories'].get(slug=category_slug)
        bread_crumb = category.__breadcrumb__().split('->')

        list_objects = []
        for cat in bread_crumb:
            list_objects.append(context['categories'].get(name=cat))

        if category.parent :
            category_items = category.sub_category.all()
        else:
            category_items = category.category.all()

        context['category_items'] = category_items
        context['category'] = category
        context['bread_crumb'] = list_objects

        return context


class ProductDetailView(CartNo, TemplateView):
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = context['all_items'].get(slug=url_slug)
        similar_product = context['all_items'].filter(category=product.category).exclude(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        context['sim_prod'] = similar_product
        return context


class AddToCartView(CartNo, View):

    def get(self, request, *args, **kwargs):
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Item.objects.get(id=product_id)
        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = NewCart.objects.get(id=cart_id)
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
                CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.display_new_selling_price, quantity=1,
                    subtotal=product_obj.display_new_selling_price)
                cart_obj.total += product_obj.display_new_selling_price
                cart_obj.save()

        else:
            """if the user is not logged in - cart object is created empty"""
            if request.user.is_authenticated:
                cart_obj = NewCart.objects.create(user = self.request.user, total=0)
            else:
                cart_obj = NewCart.objects.create(total=0)


            self.request.session['cart_id'] = cart_obj.id
            CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.display_new_selling_price, quantity=1,
                subtotal=product_obj.display_new_selling_price)
            cart_obj.total += product_obj.display_new_selling_price
            cart_obj.save()

        messages.success(request, 'Product added to the cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class MyCartView(CartNo,  TemplateView):
    template_name = "my_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ManageCartView(View):
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


class ShipOrderView(CartNo,View):

    def get(self, request, *args, **kwargs):
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = NewCart.objects.get(id=cart_id)
            order = Order.objects.create(cart = cart_obj,
                                 customer = request.user.customer,
                                 subtotal = cart_obj.total,
                                 discount = 0,
                                 total = cart_obj.total,
                                 order_status = 'CREATED')

            Delivery.objects.create(order=order,
                                    delivery_status='PROCESSING',
                                    delivery_manager=User.objects.get(pk=1))

            html_message = render_to_string('email_order_content.html', {'cart': cart_obj})

            subject = 'Your Order placed with city mart. Order # - ' + str(order.id)
            message = f'Hi, thank you for placing an order.\n'
            message = message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.request.user.email, ]
            send_mail(subject, message, email_from, recipient_list,html_message=html_message)

            del self.request.session['cart_id']
        return redirect("ecomm_app:order_placed")


class CheckoutView(CartNo, CreateView):
    template_name = "check_out.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomm_app:order_placed")
    context = {}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/?next=/check_out/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        if customer is not None and customer.full_name is not None and customer.house_no is not None:
            context['customer'] = customer
            context['customer_exist'] = 0
        else:
            context['customer_exist'] = 1
        self.context = context
        return self.context

    def form_valid(self, form):
        customer_details = form.cleaned_data
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            instance, created = Customer.objects.get_or_create(user=self.request.user)
            if not created:
                for attr, value in customer_details.items():
                    setattr(instance, attr, value)
                instance.save()

            cart_obj = NewCart.objects.get(id=cart_id)
            order = Order.objects.create(cart = cart_obj,
                                 customer = instance,
                                 subtotal = cart_obj.total,
                                 discount = 0,
                                 total = cart_obj.total,
                                 order_status = 'CREATED')

            # at this time create a delivery item that it is processing
            Delivery.objects.create(order = order,
                                    delivery_status = 'PROCESSING',
                                    delivery_manager = User.objects.get(pk=1))



            subject = 'Your Order placed with city mart. Order # - '+ str(order.id)
            message = f'Hi, thank you for placing an order.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.request.user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            del self.request.session['cart_id']
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


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(name__icontains=kw) | Q(description__icontains=kw) | Q(category__name__icontains=kw) | Q(sub_category__name__icontains=kw))

        context["results"] = results
        return context


class CancelOrderView(CartNo,TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)
        order.order_status="ORDER_CANCELLED"
        order.save()
        msg = "Your Order Order # - " + str(order.id) + " has been cancelled"
        messages.success(self.request,msg)

        subject = msg
        message = f'Hello, your order has been cancelled'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return context



def editCustomerProfileView(request):

    success_message = ""

    if request.method == "POST":

        name = request.POST['name']
        mobile = request.POST['mobile']
        house_no = request.POST['houseNo']
        street = request.POST['street']
        city = request.POST['city']
        pin = request.POST['pin']
        landmark = request.POST['landmark']

        customer = Customer.objects.filter(user=request.user)
        customer.update(user = request.user, full_name = name, mobile = mobile
                                ,house_no=house_no,street=street,city=city,pin_code=pin,landmark=landmark)
        success_message = "User "+request.user.username+" updated successfully"

    return HttpResponse({'success_message':success_message,'customer_data':customer})


class CustomerProfileView(CartNo, TemplateView):
    template_name = "customer_profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(customer=customer).all()
        context['order_items'] = orders
        context['form_submitted'] = True

        return context


class OrderDetailView(CartNo, TemplateView):
    template_name = "order_details.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)
        context['order'] = order
        context['cart'] = order.cart
        return context