from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('payment', views.payment, name='payment'),
    path('payment/<platform>/', views.payment_exec, name='payment'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug>/', views.categories_detail, name='category_detail'),
    path('shipping/', views.shipping, name='shipping'),
    path('faq/', views.frequently_asked, name='faq'),
    path('products/<slug>/', views.product_detail, name='pr-detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/p/<slug>', views.blog_post, name='blog'),

]+static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)