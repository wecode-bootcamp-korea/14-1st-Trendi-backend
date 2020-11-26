import json
from random import randint

from django.views import View
from django.http import JsonResponse

from .models import Order, OrderList, OrderStatus
from product.models import Product, Color, ProductColor, Size, ProductSize
from user.models import User
from core.utils import login_decorator

def delivery_fee_calculator(orderlists):
    sum = 0
    for orderlist in orderlists:
        sum += orderlist.product.price*orderlist.quantity
    if sum > 50000:
        orderlist.order.delivery_fee = 0
    else:
        orderlist.order.delivery_fee = 2500
    orderlist.order.save()

class OrderListView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            user     = request.user
            product  = Product.objects.get(pk=data["product_id"])
            quantity = data["quantity"]
            color_id = data.get("color_id",None)
            size_id  = data.get("size_id",None)
            order    = Order.objects.filter(user=user, orderstatus_id=1)

            if quantity < 1:
                return JsonResponse({"message":"INVALID_QUANTITY"},status=400)
            if not order.exists():
                created_order = Order.objects.create(
                    user           = user,
                    orderstatus_id = 1
                )
                year          = str(created_order.updated_at.year)
                month         = str(created_order.updated_at.month)
                day           = str(created_order.updated_at.day)
                random_number = str(randint(10000000,99999999))
                number        = year+month+day+random_number
                created_order.number = number
                created_order.save()

            current_order = order.last()
            orderlist, created = OrderList.objects.get_or_create(
                product=product,
                order=current_order,
                color_id=color_id,
                size_id=size_id
            )
            if created:
                orderlist.quantity = 0
            orderlist.quantity += quantity
            orderlist.save()

            orderlists = current_order.orderlist_set.all()
            delivery_fee_calculator(orderlists)
            return JsonResponse({"message":"SUCCESS"}, status=201)
        except Product.DoesNotExist:
            return JsonResponse({"message":"INVALID_PRODUCT"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)
    
    @login_decorator
    def get(self, request):
        orderlists = Order.objects.filter(user=request.user, orderstatus_id=1).last().orderlist_set.select_related('product__seller', 'product__delivery','size','color').all()
        orderlist_data = [{
            "orderlist_id"    : orderlist.id,
            "title"           : orderlist.product.title,
            "quantity"        : orderlist.quantity,
            "price"           : orderlist.product.price,
            "delivery"        : orderlist.product.delivery.delivery_type,
            "seller"          : orderlist.product.seller.name,
            "thumb_image_url" : orderlist.product.thumb_image_url,
            "created_at"      : orderlist.created_at,
            "updated_at"      : orderlist.updated_at,
            "size"            : orderlist.size.name if orderlist.size_id is not None else None,
            "color"           : orderlist.color.name if orderlist.color_id is not None else None,
            "delivery_fee"    : orderlist.order.delivery_fee,
            "delivery_fee1"    : orderlist.order.delivery_fee,
            "delivery_fee2"    : orderlist.order.delivery_fee,
            "delivery_fee3"    : orderlist.order.delivery_fee
        } for orderlist in orderlists]
        return JsonResponse({"data": orderlist_data}, status=200)

    @login_decorator
    def delete(self, request, id):
        try:
            user = request.user
            orderlist = OrderList.objects.get(pk=id)
            if orderlist.order.user != user:
                return JsonResponse({"message":"INVALID_USER"}, status=400)

            deleted_order_number = orderlist.order.id
            orderlist.delete()

            orderlists = OrderList.objects.select_related('product').filter(order_id=deleted_order_number)
            if orderlists.exists():
                delivery_fee_calculator(orderlists)
            else:
                Order.objects.get(pk=deleted_order_number).delete()

            return JsonResponse({"message":"SUCCESS"}, status=200)
        except OrderList.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDERLIST"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)
    
    @login_decorator
    def patch(self, request, id):
        data = json.loads(request.body)
        orderlist_id = id
        try:
            user = request.user
            quantity= data["quantity"]
            orderlist_to_update = OrderList.objects.get(pk=orderlist_id)
            if orderlist_to_update.order.user != user:
                return JsonResponse({"message":"INVALID_USER"}, status=400)
            if quantity < 1:
                return JsonResponse({"message":"INVALID_QUANTITY"}, status=400)
            orderlist_to_update.quantity = quantity
            orderlist_to_update.save()

            orderlists = Order.objects.filter(user=user, orderstatus_id=1).last().orderlist_set.select_related('product').all()
            delivery_fee_calculator(orderlists)
            return JsonResponse({"message":"SUCCESS"}, status=200)
        except OrderList.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDERLIST"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)