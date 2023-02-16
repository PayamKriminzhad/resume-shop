from cgitb import lookup
from re import T
from django.db import models
from django.db.models import Q
import os
from django.db.models.signals import pre_save, post_save

from categories.models import Category


def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/{final_name}"

def upload_image_path_incoming(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/incoming/{final_name}"

def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/galleries/{final_name}"



class ProductManager(models.Manager):

    def get_active_products(self):
        return self.get_queryset().filter(active = True)
    
    def get_products_by_category(self, category):
        return self.get_queryset().filter(categories__name__iexact = category, active = True)

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id = product_id)

        if qs.count() == 1:
            return qs.first()
        else:
            return None
        
    def search(self, query):
        lookup = (
            Q(title__icontains = query) |
            Q(description__icontains = query) |
            Q(tag__title__icontains = query) |
            Q(categories__title__icontains = query)
        )
        return self.get_queryset().filter(lookup, active = True)
    
class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    price_discount = models.IntegerField(verbose_name='قیمت با تخفیف', null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    categories = models.ManyToManyField(Category, blank=True, verbose_name="دسته بندی ها")
    visit_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    discount = models.FloatField(default=0, verbose_name='تخفیف')

    objects = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_discount(self):
        return int(self.discount * 100)

    def final_price(self):
        return int(self.price - (self.price * self.discount))

    def get_absolute_url(self):
        return f"/products/{self.id}/{self.title.replace(' ', '-')}"

def discount(sender, instance, *args, **kwargs):
    instance.price_discount=instance.final_price()

pre_save.connect(discount, sender=Product)


class ProductGallery(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    image = models.ImageField(upload_to=upload_gallery_image_path, verbose_name='تصویر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return self.title

    
class ProductComment(models.Model):
    name = models.CharField(max_length=150, verbose_name='فرستنده')
    email = models.EmailField(max_length=150, verbose_name='ایمیل')
    massage = models.TextField(verbose_name='نظر')
    date = models.DateField(blank=True, null=True, verbose_name='تاریخ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return self.name

    
class IncomingProduct(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to=upload_image_path_incoming, null=True, blank=True, verbose_name='تصویر')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    categories = models.ManyToManyField(Category, blank=True, verbose_name="دسته بندی ها")
    date = models.DateField(null=True)

    class Meta:
        verbose_name = 'محصول در راه'
        verbose_name_plural = 'محصولات در راه'

    def __str__(self):
        return self.title