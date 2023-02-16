from genericpath import exists
import itertools
from django import http
from django.shortcuts import redirect, render
from django.http import Http404
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth import authenticate
import datetime

from .forms import CommentForm
from .models import Product, ProductManager, ProductGallery, ProductComment
from categories.models import Category
from orders.forms import UserNewOrderForm, UserNewOrderFormForComponent
from accounts.models import Dashbord

class ProductList(ListView):
    template_name = 'products_list.html'
    paginate_by = 8

    def get_queryset(self):
        price_range = self.request.GET.get('f')
        products = Product.objects.get_active_products()
        if price_range is not None:
            result = [int(x) for x in price_range.split() if x.isdigit()]
            return products.filter(price_discount__range=(result[1], result[0]))
        return products



class ProductListByCategory(ListView):
    template_name = 'products_list.html'
    paginate_by = 8

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        price_range = self.request.GET.get('f')
        category = Category.objects.filter(name__iexact=category_name)
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
        products_by_category = Product.objects.get_products_by_category(category_name)
        if price_range is not None:
            result = [int(x) for x in price_range.split() if x.isdigit()]
            return products_by_category.filter(price_discount__range=(result[1], result[0]))
        return Product.objects.get_products_by_category(category_name)

class ProductSearch(ListView):
    template_name = 'products_list.html'
    paginate_by = 8

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        price_range = request.GET.get('f')
        if query is not None:
            products = Product.objects.search(query).distinct()
            if price_range is not None:
                result = [int(x) for x in price_range.split() if x.isdigit()]
                return products.filter(price_discount__range=(result[1], result[0]))
            return Product.objects.search(query).distinct()
        return Product.objects.get_active_products().distinct()

class ProductFilter(ListView):
    template_name = 'products_list.html'
    paginate_by = 8
    
    def get_queryset(self):
        request = self.request
        price = request.GET.get('f')
        result = [int(x) for x in price.split() if x.isdigit()]
        if result is not None:
            return Product.objects.filter(price_discount__range=(result[1], result[0]))
        return Product.objects.get_active_products()

def price_range_partial(request, url):
    value = request.GET.get('f')
    context = {
        'value' : value,
        'url' : url
    }
    return render(request, 'price_range.html', context)

def products_categories_partial(request, url):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'url' : url
    }
    return render(request, 'products_categories_partial.html', context)

def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, *args, **kwargs):

    productId = kwargs['productId']
    product = Product.objects.get_by_id(productId)

    if product is None or not product.active:
        return Http404

    category_name = product.categories.first()
    related_products = Product.objects.filter(~Q(id=productId), categories__product=product).distinct()[:4]

    order_form = UserNewOrderForm(request.POST or None, initial={'product_id':productId})

    gallery = ProductGallery.objects.filter(product_id=productId)
    grouped_gallery = list(my_grouper(3, gallery))

    comment_form = CommentForm(request.POST or None, initial={'product_id':productId, 'date':datetime.date.today()})
    if comment_form.is_valid():
        name = comment_form.cleaned_data.get('name')
        email = comment_form.cleaned_data.get('email')
        massage = comment_form.cleaned_data.get('massage')
        date = comment_form.cleaned_data.get('date')
        motherID = comment_form.cleaned_data.get('product_id')

        ProductComment.objects.create(product_id=motherID, name=name, email=email, massage=massage, date=date)
        return redirect(f'{product.get_absolute_url()}')
    comments = product.productcomment_set.all()

    context = {
        'product': product,
        'gallery': grouped_gallery,
        'related': related_products,
        'category': category_name,
        'orderform':order_form,
        'commentform':comment_form,
        'comments':comments
    }
        

    return render(request, 'product_detail.html', context)

def product_component(request, product):
    order_form = UserNewOrderFormForComponent(request.POST or None, initial={'product_id':product.id, 'count':1})
        
    context ={
        'product': product,
        'form':order_form,
        'is_liked': False,
        'is_new': False
    }
    if request.user.is_authenticated:
        user_id = request.user.id
        dashbord = Dashbord.objects.filter(owner_id=user_id).first()
        liked = dashbord.liked.filter(id=product.id).first()
        if liked is not None:
            context['is_liked'] = True

    latest_products = Product.objects.order_by('-id').all()[:8]
    if product in latest_products:
        context['is_new'] = True

    return render(request, 'product_item_component.html', context)
