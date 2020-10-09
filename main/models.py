from django.db import models
import json
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.
social_links = [
    {
        'social': True,
        'classes': 'fab fa-whatsapp-square',
        'handle': '+254 773 362 921',
        'link': 'https://api.whatsapp.com/send?phone=254773362921'
    },
    {
        'social': True,
        'classes': 'fab fa-instagram',
        'handle': '@curiokenya',
        'link': 'https://instagram.com/curiokenya'
    },
    {
        'social': True,
        'classes': 'fab fa-facebook',
        'handle': 'Curio Kenya',
        'link': 'https://www.facebook.com/CurioKenya8'
    },
    {
        'social': True,
        'classes': 'fab fa-twitter-square',
        'handle': '@curio_kenya',
        'link': 'https://twitter.com/curio_kenya'
    },
    {
        'social': True,
        'classes': 'fab fa-pinterest',
        'handle': 'CurioKenya',
        'link': 'https://www.pinterest.ch/CurioKenya/'
    },
    {
        'social': False,
        'classes': 'fas fa-map-marker-alt',
        'handle': 'LIKONI ROAD',
        'link': '#'
    },
    {
        'social': False,
        'classes': 'fas fa-globe-africa',
        'handle': 'NAIROBI, KENYA',
        'link': '#'
    },
    {
        'social': False,
        'classes': 'fas fa-envelope',
        'handle': 'betinaawuor@gmail.com',
        'link': 'mailto:betinaawour@gmail.com'
    },
    {
        'social': False,
        'classes': 'fas fa-phone-alt',
        'handle': '+254 773 362 921',
        'link': 'tel:+254 773 362 921'
    },
]


class Category(models.Model):
    slug = models.CharField(max_length=300, null=False,
                            blank=True, unique=True, editable=False)
    name = models.CharField(max_length=255, blank=False,
                            null=False, unique=True)
    image = models.ImageField(upload_to='categories',
                              default='category.png', blank=False)
    active = models.BooleanField(default=True, blank=False, null=False)
    date = models.DateField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def save(self):
        self.slug = (self.name.lower()).replace(' ', '-')
        super().save()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering =['-date']

    def __str__(self):
        return self.name


class Product(models.Model):
    slug = models.CharField(max_length=300, null=False,
                            blank=True, unique=True, editable=False,)
    name = models.CharField(max_length=200, null=False,
                            blank=False, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    specifications = models.TextField()
    description = models.TextField()
    ksh_price = models.FloatField(default=0)
    usd_price = models.FloatField(default=0, editable=False)
    available = models.BooleanField(default=True, blank=False, null=False)
    clicks = models.IntegerField(default=0, editable=False)
    date = models.DateField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def save(self):
        self.slug = (self.name.lower()).replace(' ', '-')
        user_settings = {}
        try:
            with open('settings.json', 'r') as settings_file:
                user_settings = json.load(settings_file)
                settings_file.close()
        except:
            pass
        ksh_to_usd = user_settings.get(
            'default', {}).get('USD_exchange_rate', 100)
        self.usd_price = round(self.ksh_price/ksh_to_usd,3)
        super().save()

    @classmethod
    def get_by_slug(cls, slug, available=True):
        return cls.objects.filter(category__slug=slug, available=available)

    @classmethod
    def get_all(cls, available=True):
        return cls.objects.filter(available=available)

    @classmethod
    def get_top(cls, available=True):
        return cls.objects.filter(available=available)[0:10]
    
    class Meta:
        ordering=['-clicks', '-date']

    def __str__(self):
        return '%s' % (self.name)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products', blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.product.name)

@receiver(pre_delete, sender=ProductImage)
def delete_product_images(sender, instance, **kwargs):
    instance.image.delete()

@receiver(pre_delete, sender=Category)
def delete_product_images(sender, instance, **kwargs):
    instance.image.delete()