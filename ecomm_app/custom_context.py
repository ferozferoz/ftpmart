from .models import *
from django.shortcuts import get_object_or_404
from ecomm_manage_app.models import *
from django.db.models import Q


def render_ecomm_app_context(request):

    cart_id = request.session.get("cart_id", None)
    if cart_id:
        cart = get_object_or_404(NewCart, id=cart_id)
    else:
        cart = None
    context = {'cart': cart, 'categories': Category.objects.all(),
               'category_nav': Category.objects.filter(parent_id=None),
               'all_items': Item.objects.filter(is_active=True),
               'is_manager': request.user.groups.filter(Q(name='inventory') | Q(name='delivery')).exists()}
    return context