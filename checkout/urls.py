from django.urls import path
from . import views

urlpatterns=[
    path('summary/',views.cart, name='cart_summary')
]