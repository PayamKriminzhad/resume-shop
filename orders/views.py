import time
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from zeep import Client

from .forms import UserNewOrderForm
from .models import Order, OrderDetail
from products.models import Product

@login_required(login_url='/login')
def add_user_order(request):
    new_order = UserNewOrderForm(request.POST or None)
    if new_order.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()

        if order is None:
            order=Order.objects.create(owner_id=request.user.id, is_paid=False)

        product_id = new_order.cleaned_data.get('product_id')
        count = new_order.cleaned_data.get('count')
        if count < 1 :
            count = 1

        product = Product.objects.get_by_id(product_id)

        if_product_exists: OrderDetail = order.orderdetail_set.filter(product_id=product_id).first()
        if if_product_exists is not None:
            if_product_exists.count += count
            if_product_exists.save()
        else:
            order.orderdetail_set.create(product_id=product_id, count=count)
        return redirect(f'{product.get_absolute_url()}')
        print('123')
    return redirect('/')
    

@login_required(login_url='/login')
def open_user_order(request):

    context = {
        'order':None,
        'detail':None,
        'total':0
    }

    order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if order is not None:
        context['order'] = order
        context['details'] = order.orderdetail_set.all()
        context['total'] = order.get_total_price

    return render(request, 'cart.html', context)


@login_required(login_url='/login')
def remove_order_detail(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()
            return redirect('/open-order')
    raise Http404()



# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# amount = 1000  # Toman / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional

# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# CallbackURL = 'http://localhost:8000/verify'  # Important: need to edit for realy server.

# def send_request(request, *args, **kwargs):
#     total_price = 0
#     open_order: Order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
#     if open_order is not None and open_order.get_total_price() > 0:
#         total_price = open_order.get_total_price()
#         result = client.service.PaymentRequest(
#             MERCHANT, total_price, description, email, mobile, f"{CallbackURL}/{open_order.id}"
#         )
#         if result.Status == 100:
#             return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
#         else:
#             return HttpResponse('Error code: ' + str(result.Status))
#     raise Http404()


# def verify(request, *args, **kwargs):
#     order_id = kwargs.get('order_id')
#     if request.GET.get('Status') == 'OK':
#         result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
#         if result.Status == 100:
#             user_order = Order.objects.get_queryset().get(id=order_id)
#             user_order.is_paid = True
#             user_order.payment_date = time.time()
#             user_order.save()
#             return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
#         elif result.Status == 101:
#             return HttpResponse('Transaction submitted : ' + str(result.Status))
#         else:
#             return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
#     else:
#         return HttpResponse('Transaction failed or canceled by user')
