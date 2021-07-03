from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from user_management_app.models import Customer

from django.utils.timezone import now


# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self',blank=True, null=True, related_name='child', on_delete=models.CASCADE)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return '->'.join(reversed(full_path))


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    home_phone = PhoneNumberField(null=False, blank=False, unique=True)
    office_phone = PhoneNumberField(null=False, blank=False, unique=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.seller_name


class Item(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='sub_category')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    sell_quantity = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products")
    cost_price = models.DecimalField( max_digits=10, decimal_places=2)
    display_original_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    display_new_selling_price = models.DecimalField(max_digits=10,  decimal_places=2)
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True) # will create a table later
    return_policy = models.CharField(max_length=300, null=True, blank=True) # will create a table later
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


ORDER_STATUS = (
    ("ORDER RECEIVED", "ORDER_RECEIVED"),
    ("ORDER PROCESSING", "ORDER_PROCESSING"),
    ("ON THE WAY", "ON_THE_WAY"),
    ("ORDER COMPLETED", "ORDER_COMPLETED"),
    ("ORDER CANCELLED", "ORDER_CANCELLED"),
    ("RETURN REQUESTED","RETURN_REQUESTED"),
)

PAYMENT_METHOD = (
    ("CASH ON DELIVERY", "CASH_ON_DELIVERY"),
    ("GPAY", "GPAY"),
    ("CREDIT CARD", "CREDIT_CARD"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #ordered_by = models.CharField(max_length=200)
    #shipping_address = models.CharField(max_length=200)
    #mobile = models.CharField(max_length=10)
    #email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "Order: " + str(self.id)


class ProductImage(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
