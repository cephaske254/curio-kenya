from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, response
from django.core.serializers import serialize
from main.models import Product
from .cart import Cart
from django.views.decorators.csrf import csrf_exempt
import json

# @require_POST


@csrf_exempt
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST' and request.POST.get('quantity'):
        cart.add(product = product, quantity = request.POST.get(
            'quantity'), update_quantity = True)
    else:
        cart.add(product = product)

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart=Cart(request)
    cart.remove(product_id)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart=Cart(request).cart
    for cart_item in cart:
        item_from_db = Product.objects.filter(pk=cart_item).first()
        if not item_from_db:
            cart.remove(cart_item)
        else:
            cart[cart_item]['ksh_price'] = item_from_db.ksh_price
            cart[cart_item]['usd_price'] = item_from_db.usd_price
    return response.JsonResponse(cart, safe = False)
