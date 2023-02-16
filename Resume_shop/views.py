from django.shortcuts import render

from products.models import IncomingProduct, Product
from dynamics.models import SiteSetting
from orders.models import Order


def header(request):
    setting = SiteSetting.objects.first()
    context = {
        'setting':setting
    }

    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(owner_id=user.id).first()
        context['user'] = user
        context['order'] = order

    return render(request, 'shared/Header.html', context)

def footer(request):
    setting = SiteSetting.objects.first()

    context = {
        'setting':setting
    }

    return render(request, 'shared/Footer.html', context)

def home_page(request):

    income = IncomingProduct.objects.all()
    setting = SiteSetting.objects.first()

    categories = setting.category_set.all()

    latest_products = Product.objects.order_by('-id').all()[:8]

    most_visited = Product.objects.order_by('-visit_count').all()[:8]

    context = {
        'income':income,
        'setting':setting,
        'categories':categories,
        'latest':latest_products,
        'visited':most_visited
    }
    return render(request, 'home_page.html', context)