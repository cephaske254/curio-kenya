from django.conf import settings
from main.models import Product
from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            try:
                image = product.images.first().image.url
            except:
                image = None
                
            self.cart[product_id] = {
                'name': product.name,
                'quantity': 1,
                'ksh_price': str(product.ksh_price),
                'usd_price': str(product.usd_price),
                'image': image
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        if str(product_id) in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['usd_price'] = Decimal(item['usd_price'])
            item['ksh_price'] = Decimal(item['ksh_price'])
            item['total_price'] = item['ksh_price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_ksh_price(self):
        return sum(Decimal(item['ksh_price']) * item['quantity'] for item in self.cart.values())

    def get_total_usd_price(self):
        return sum(Decimal(item['usd_price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
