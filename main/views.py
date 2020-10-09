from django.shortcuts import render, Http404
from main.models import social_links, Category, Product
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from decouple import config
from django.http.response import HttpResponse, JsonResponse
import json
from checkout.core.paypal_checkout import CreateOrder
from django.core import serializers


def index(request):
    products = Product.get_top()
    context = {
        'products':products
    }
    return render(request, 'main/index.html', context=context)


def payment(request):
    context = {
    }
    return render(request, 'main/payment.html', context=context)


def payment_exec(request, *args, **kwargs):
    context = {
    }
    order_data = CreateOrder().create_order()
    response = {
        "orderID": order_data.result.id
    }

    return JsonResponse(response, safe=False)


def contact(request):
    context = {
        'title': 'Contact',
    }
    return render(request, 'main/contact.html', context=context)


def shop(request):
    page = request.GET.get('page', 1)
    product_list = Paginator(Product.get_all(),24,allow_empty_first_page=True)
    try:
        products = product_list.page(page)
    except EmptyPage:
        products = product_list.page(product_list.num_pages)
    except PageNotAnInteger:
        products = product_list.page(product_list.num_pages)

    context = {
        'title': 'Shop',
        'products': products
    }
    return render(request, 'main/shop.html', context=context)


def shipping(request):
    context = {
        'title': 'Shipping & Returns',
    }
    return render(request, 'main/shipping.html', context=context)


def categories(request):
    category_list = Paginator(Category.objects.filter(
        active=True).all(), 24, allow_empty_first_page=True)

    page = request.GET.get('page', 1, )
    try:
        categories = category_list.page(page)
    except EmptyPage:
        categories = category_list.page(category_list.num_pages)
    except PageNotAnInteger:
        categories = category_list.page(1)
    context = {
        'title': 'Categories',
        'categories': categories,
    }
    return render(request, 'main/categories.html', context=context)


def categories_detail(request, slug):
    page = request.GET.get('page', 1, )
    category_object = Category.objects.filter(slug=slug, active=True).first()

    if not category_object:
        raise Http404()

    product_list = Paginator(Product.get_by_slug(
        slug), 24, allow_empty_first_page=True)
    try:
        products = product_list.page(page)
    except EmptyPage:
        products = product_list.page(product_list.num_pages)
    except PageNotAnInteger:
        products = product_list.page(1)

    context = {
        'title': category_object.name.title(),
        'products': products
    }
    return render(request, 'main/category.html', context=context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_images = product.images.all()
    similar_products = Product.objects.filter(Q(slug=slug) | Q(
        category=product.category)).exclude(slug=slug)[:4]
    context = {
        'title': product.name.title(),
        'product': product,
        'images_range': list(range(len(product_images))),
        'product_images': product_images,
        'similar_products': similar_products
    }
    return render(request, 'main/product.html', context=context)


def frequently_asked(request):
    context = {
        'title': 'FAQ',
    }

    return render(request, 'main/faq.html', context=context)


def blog(request):
    context = {
        'title': 'Contact',
    }
    return render(request, 'main/blog.html', context=context)


def blog_post(request):
    context = {
        'title': 'Contact',
    }
    return render(request, 'main/contact.html', context=context)
