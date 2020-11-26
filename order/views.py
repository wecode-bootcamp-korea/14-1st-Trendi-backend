import json
from random import randint

from django.views import View
from django.http import JsonResponse

from .models import Order, OrderList, OrderStatus
from product.models import Product, Color, ProductColor, Size, ProductSize
from user.models import User

def delivery_fee_calculator(orderlists, current_order):
    sum = 0
    for orderlist in orderlists:
        sum += orderlist.product.price*orderlist.quantity
    if sum > 50000:
        current_order.delivery_fee = 0
        current_order.save()
    else:
        current_order.delivery_fee = 2500
        current_order.save()

class OrderListView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user     = User.objects.get(pk=data["user_id"])
            quantity = data["quantity"]
            product  = Product.objects.get(pk=data["product_id"])
            color    = data.get("color",0)
            size     = data.get("size",0)
            order    = Order.objects.filter(user_id=user_id, status_id=1)
            
            if not order.exists():
                created_order = Order.objects.create(
                    user         = user,
                    status_id    = 1
            )
                year          = str(created_order.updated_at.year)
                month         = str(created_order.updated_at.month)
                day           = str(created_order.updated_at.day)
                random_number = str(randint(10000000,99999999))
                number        = year+month+day+random_number
                created_order.number = number
                created_order.save()

            current_order = order.last()
            existing_orderlist = OrderList.objects.filter(product=product, order=current_order, color=color, size=size)
            if existing_orderlist.exists():
                existing_orderlist.update(quantity=existing_orderlist.first().quantity + quantity)
                existing_orderlist.first().save()
            else:
                OrderList.objects.create(
                    quantity = quantity,
                    product  = product,
                    order    = current_order,
                    color    = color,
                    size     = size
                )
            orderlists = current_order.orderlist_set.all()
            print("------orderlists-------",orderlists)
            delivery_fee_calculator(orderlists, current_order)

            return JsonResponse({"message":"SUCCESS"}, status=201)
        except Product.DoesNotExist:
            return JsonResponse({"message":"INVALID_PRODUCT"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)
    
    def get(self, request, id):
        user_id = id
        user = User.objects.get(pk=user_id)
        try:
            order = Order.objects.get(user=user, status_id=1)
            orderlists = OrderList.objects.filter(order=order)
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
                "size"            : orderlist.product.productsize_set.get(size_id=orderlist.size).size.name if orderlist.size != 0 else None,
                "color"           : orderlist.product.productcolor_set.get(color_id=orderlist.color).color.name if orderlist.color != 0 else None
            } for orderlist in orderlists]
            return JsonResponse({"data": orderlist_data}, status=200)
        except OrderList.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDERLIST"}, status=400)
    
    def delete(self, request, id):
        try:
            user = request.GET["user_id"]
            orderlist_id = id
            
            user = User.objects.get(pk=user)
            orderlist_to_delete = OrderList.objects.get(pk=orderlist_id)

            if orderlist_to_delete.order.user != user:
                return JsonResponse({"message":"INVALID_USER"}, status=400)

            deleted_order_number = orderlist_to_delete.order.id
            orderlist_to_delete.delete()
            if not OrderList.objects.filter(order_id=deleted_order_number).exists():
                Order.objects.get(pk=deleted_order_number).delete()
            
            order = Order.objects.get(user=user, status_id=1)
            orderlists = order.orderlist_set.all()
            delivery_fee_calculator(orderlists, order)
            return JsonResponse({"message":"SUCCESS"}, status=200)
        except OrderList.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDERLIST"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)
    
    def patch(self, request, id):
        data = json.loads(request.body)
        orderlist_id = id
        try:
            user = User.objects.get(pk=data["user_id"])
            quantity= data["quantity"]
            orderlist_to_update = OrderList.objects.get(pk=orderlist_id)
            if orderlist_to_update.order.user != user:
                return JsonResponse({"message":"INVALID_USER"}, status=400)
            if quantity < 1:
                return JsonResponse({"message":"INVALID_QUANTITY"}, status=400)
            orderlist_to_update.quantity = quantity
            orderlist_to_update.save()

            order = Order.objects.get(user=user, status=1)
            orderlists = order.orderlist_set.all()
            delivery_fee_calculator(orderlists, order)
            return JsonResponse({"message":"SUCCESS"}, status=200)
        except OrderList.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDERLIST"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)

class OrderView(View):

    pass
