from django.contrib import admin

from main.models import Category,Product,ProductImage

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('usd_price','clicks','slug')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
