import os

from django.db import models


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.title}{ext}"
    return f"logo-image/{final_name}"
    

def upload_categoryimage_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.category}{ext}"
    return f"categories/{final_name}"



class SiteSetting(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان سایت')
    home_sentence = models.CharField(max_length=150, verbose_name='جمله اول')
    address = models.CharField(max_length=400, verbose_name='آدرس')
    phone = models.CharField(max_length=50, verbose_name='تلفن')
    mobile = models.CharField(max_length=50, verbose_name='تلفن همراه')
    fax = models.CharField(max_length=50, verbose_name='فکس')
    email = models.EmailField(max_length=50, verbose_name='ایمیل')
    about_us = models.TextField(verbose_name='درباره ما', null=True, blank=True)
    copy_right = models.CharField(verbose_name='متن کپی رایت', null=True, blank=True, max_length=200)
    logo_image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر لوگو')
    facebook = models.CharField(max_length=250, verbose_name='فیس بوک')
    instagram = models.CharField(max_length=250, verbose_name='اینستاگرام')
    tweeter = models.CharField(max_length=250, verbose_name='توییتر')
    skype = models.CharField(max_length=250, verbose_name='اسکایپ')


    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'مدیریت تنظیمات'

    def __str__(self):
        return self.title


class Category(models.Model):
    mother = models.ForeignKey(SiteSetting, on_delete=models.CASCADE)
    category = models.CharField(max_length=150, verbose_name='دسته بندی')
    ref = models.CharField(max_length=150, verbose_name='آدرس')
    image = models.ImageField(upload_to=upload_categoryimage_path, null=True, blank=True, verbose_name='تصویر')
    

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.category
