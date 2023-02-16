from django.db import models
import os
from django.contrib.auth.models import User

from products.models import Product


def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.u_name}{ext}"
    return f"profiles/{final_name}"



    
class Dashbord(models.Model):
    profile = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر', default='profiles/0.png')
    u_name = models.CharField(max_length=50, verbose_name='نام کاربری')
    f_name = models.CharField(max_length=50, verbose_name='نام', null=True, blank=True,)
    l_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', null=True, blank=True,)
    ph_number = models.CharField(max_length=50, verbose_name='تلفن همراه', null=True, blank=True,)
    email = models.EmailField(max_length=100, verbose_name='ایمیل', null=True, blank=True,)
    liked = models.ManyToManyField(Product, blank=True, verbose_name='مورد علاقه ها')
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.u_name
