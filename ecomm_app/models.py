from django.db import models

from ecomm_manage_app.models import Item
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    house_no = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=15)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class NewCart(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(NewCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


class Order(models.Model):

    ORDER_STATUS = (
        ("CREATED", "Created",),
        ("COMPLETE", "Complete",),
        ("CANCELLED", "Cancelled"),

    )

    cart = models.OneToOneField(NewCart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.order_status)

class Delivery(models.Model):

    DELIVERY_STATUS = (
        ("PROCESSING", "Processing",),
        ("PICKED", "Picked"),
        ("DELIVERED", "Delivered"),
        ("ABORTED", "Aborted"),

    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=50, choices=DELIVERY_STATUS)
    delivery_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Delivery: " + str(self.delivery_status)
