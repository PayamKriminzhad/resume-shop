from django.contrib import admin

from .models import Product, ProductGallery, IncomingProduct, ProductComment


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'price', 'active']
    list_editable = ['price', 'active']

    class Meta:
        model = Product

class IncomingProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'active']
    list_editable = ['title', 'active']

    class Meta:
        model = IncomingProduct


admin.site.register(Product, ProductAdmin)
admin.site.register(IncomingProduct, IncomingProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(ProductComment)