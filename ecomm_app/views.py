from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.utils.html import strip_tags
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm,CheckoutForm
from django.contrib import messages
from user_management_app.views import *
from ecomm_manage_app.models import Category
from django.template.loader import render_to_string
from ecomm_app.custom_context import render_ecomm_app_context
from django.core.paginator import Paginator

"""Mixin class -- will be deleted"""

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
        context['all_items'] = Item.objects.filter(is_active=True)
        context['is_manager'] = self.request.user.groups.filter(Q(name='inventory') | Q(name='delivery')).exists()
        return context


"""Function return Main page"""


class HomeView(TemplateView):
    template_name = "ecomm_app/home.html"


class CategoryProductsView(TemplateView):

    template_name = "ecomm_app/shop_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        category_items = category.category.all()
        paginator = Paginator(category_items,3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['category_items'] = page_obj
        context['category'] = category

        return context


class SubCategoryProductsView(TemplateView):

    template_name = "ecomm_app/shop_subcategory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        category_items = category.sub_category.all()
        paginator = Paginator(category_items, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['sub_category_items'] = page_obj
        context['sub_category'] = category

        return context


class ProductDetailView(View):

    template_name = "ecomm_app/product_detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        url_slug = self.kwargs['slug']
        custom_context = render_ecomm_app_context(self.request)
        product = custom_context['all_items'].get(slug=url_slug)
        similar_product = custom_context['all_items'].filter(category=product.category).exclude(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        context['sim_prod'] = similar_product
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        quantity = int(request.POST.get("quantity",1))
        product_id = request.POST.get("item_id", "")
        try:
            product_obj = Item.objects.get(id=product_id)
        except Item.DoesNotExist:
            raise Http404("Product does not exist")

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            try:
                cart_obj = NewCart.objects.get(id=cart_id)
            except NewCart.DoesNotExist:
                raise Http404("Cart does not exist")

            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cart_product = this_product_in_cart.last()
                cart_product.quantity += quantity
                cart_product.subtotal += product_obj.display_new_selling_price * quantity
                cart_product.save()
                cart_obj.total += product_obj.display_new_selling_price *quantity
                cart_obj.save()
            # new item is added in cart
            else:
                CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.display_new_selling_price, quantity=quantity,
                    subtotal=product_obj.display_new_selling_price)
                cart_obj.total += product_obj.display_new_selling_price * quantity
                cart_obj.save()

        else:
            """if the user is not logged in - cart object is created empty"""
            if request.user.is_authenticated:
                cart_obj = NewCart.objects.create(user = self.request.user, total=0)
            else:
                cart_obj = NewCart.objects.create(total=0)

            self.request.session['cart_id'] = cart_obj.id
            CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.display_new_selling_price, quantity=quantity,
                subtotal=product_obj.display_new_selling_price)
            cart_obj.total += product_obj.display_new_selling_price * quantity
            cart_obj.save()

        messages.success(request, 'Product added to the cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        try:
            product_obj = Item.objects.get(id=product_id)
        except Item.DoesNotExist:
            raise Http404("Product does not exist")

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            try:
                cart_obj = NewCart.objects.get(id=cart_id)
            except NewCart.DoesNotExist:
                raise Http404("Cart does not exist")

            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

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


class ManageCartView(View):

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        try:
            action = request.GET.get("action")
        except:
            raise Http404("Incorrect request")


        try:
            cp_obj = CartProduct.objects.get(id=cp_id)
        except CartProduct.DoesNotExist:
            raise Http404("Product do not exist in Cart")


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


class MyCartView(TemplateView):

    template_name = "ecomm_app/my_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = render_ecomm_app_context(self.request)['cart']

        if cart:
            total_cart_value = getattr(cart, "total")

            if total_cart_value > 200:
                context['shipping'] = 0
            else:
                context['shipping'] = 10
        return context


class CheckoutView(View):

    template_name = "ecomm_app/check_out.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/?next=/check_out/")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {}
        cart = render_ecomm_app_context(self.request)['cart']
        total_cart_value = getattr(cart, "total")

        if total_cart_value > 200:
            context['shipping'] = 0
        else:
            context['shipping'] = 10

        customer = Customer.objects.get(user=self.request.user)

        if customer is not None and customer.full_name is not None and customer.house_no is not None:
            context['customer'] = customer
            context['customer_exist'] = 0
        else:
            context['customer_exist'] = 1

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        instance = Customer.objects.get(user=self.request.user)
        instance.full_name = request.POST.get("full_name")
        instance.house_no =  request.POST.get("house_no"),
        instance.street = request.POST.get("street"),
        instance.city = request.POST.get("city"),
        instance.pin_code = request.POST.get("pin_code"),
        instance.landmark = request.POST.get("landmark")
        instance.save()

        cart_id = self.request.session.get("cart_id", None)
        cart_obj = NewCart.objects.get(id=cart_id)
        order = Order.objects.create(cart=cart_obj,
                                     customer=instance,
                                     subtotal=cart_obj.total,
                                     discount=0,
                                     total=cart_obj.total,
                                     order_status='CREATED')

        # at this time create a delivery item that it is processing
        Delivery.objects.create(order=order,
                                delivery_status='PROCESSING',
                                delivery_manager=User.objects.get(pk=1))

        subject = 'Your Order placed with city mart. Order # - ' + str(order.id)
        message = f'Hi, thank you for placing an order.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        del self.request.session['cart_id']

        return redirect("ecomm_app:order_placed")





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

            html_message = render_to_string('ecomm_app/email_order_content.html', {'cart': cart_obj})
            subject = 'Your Order placed with city mart. Order # - ' + str(order.id)
            message = f'Hi, thank you for placing an order.\n'
            message = message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.request.user.email, ]
            send_mail(subject, message, email_from, recipient_list,html_message=html_message)

            del self.request.session['cart_id']
        return redirect("ecomm_app:order_placed")


class OrderPlacedView(CartNo, TemplateView):
    template_name = "ecomm_app/order_done.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect("ecomm_app:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        order = Order.objects.filter(customer=customer).order_by("-id")[0]
        # order_id=orders.id
        cart_products = CartProduct.objects.filter(cart=order.cart)
        context['cart_products'] = cart_products
        context['orders'] = order

        cart = order.cart
        print("printing cart")
        print(cart)

        total_cart_value = getattr(cart, "total")
        context["total"] = total_cart_value

        if total_cart_value > 200:
            context['shipping'] = 0
        else:
            context['shipping'] = 10

        return context


class SearchView(TemplateView):
    template_name = "ecomm_app/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("search-box")
        selected_category = self.request.GET.get("select-category")
        print(selected_category)
        if selected_category == "All":
            results = Item.objects.filter(Q(name__icontains=kw) | Q(description__icontains=kw) | Q(category__name__icontains=kw) | Q(sub_category__name__icontains=kw))
        else:
            results = Item.objects.filter(
                Q(category__name__icontains=selected_category) & (Q(name__icontains=kw) | Q(description__icontains=kw) |
                Q(sub_category__name__icontains=kw)))

        context["results"] = results
        context["keyword"] = kw
        context["selected_category"] = selected_category


        return context


class CancelOrderView(TemplateView):

    template_name = 'ecomm_app/home.html'

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


class CustomerProfileView(CartNo, TemplateView):
    template_name = "ecomm_app/customer_profile.html"

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
    template_name = "ecomm_app/order_details.html"

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


class RegistrationView(View):
    template_name = 'ecomm_app/customer_registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            print("form was valid")
            otp = str(random.randint(1000, 9999))
            # send_otp(mobile,otp)
            request.session['mobile'] = request.POST.get('mobile')
            request.session['email'] = request.POST.get('email')
            request.session['name'] = request.POST.get('name')
            request.session['otp'] = otp

        return redirect("ecomm_app:register_otp")


class RegisterOTPView(View):

    template_name = 'ecomm_app/otp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request):
        context = {'otp': request.session['otp']}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        key = request.POST.get('otp')
        if key == request.session['otp']:
            user = User(username=request.session['email'], email=request.session['email'],
                        first_name=request.session['name'])
            user.save()
            customer = Customer(user=user, mobile=request.session['mobile'])
            customer.save()
            login(request, user)
            return redirect("ecomm_app:home")


class LoginView(View):
    template_name = 'ecomm_app/customer_login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        mobile = request.POST.get('mobile')
        user = Customer.objects.filter(mobile=mobile).first()

        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'ecomm_app/customer_login.html', context)

        otp = str(random.randint(1000, 9999))
        request.session['otp'] = otp
        #send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('ecomm_app:login_otp')


class LoginOTPView(View):

    template_name = 'ecomm_app/otp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {'otp': request.session['otp']}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        key = request.POST.get('otp')

        if key == request.session['otp']:
            customer = Customer.objects.get(mobile=request.session['mobile'])
            login(request, customer.user)

            if "next" in request.GET:
                next_url = request.GET.get("next")
                return redirect(next_url)
            else:
                return redirect("ecomm_app:home")

        else:

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': request.session['mobile']}
            return render(request, 'ecomm_app/otp.html', context)


class LogoutView(View):

    redirect_url="ecomm_app:home"

    def get(self, request):
        logout(request)
        return redirect(self.redirect_url)

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
