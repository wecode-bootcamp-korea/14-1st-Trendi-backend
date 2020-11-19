import json

from django.views import View
from django.http import JsonResponse

from .models import Order, OrderList
from product.models import Product

class OrderView(View):
    def post(self, request):
        data=json.loads(request.body)

        try:
            data["number"]
            data["delevery_fee"]
            user_id
            status_id

class OrderStatusView(View):
    def post(self, request):
        data=json.loads(request.body)
        try:
            status = data["status"]

            if status is not 1 or 2 or 3:
                return JsonResponse({"message":"out of order status!!"}, status=400)
            
            OrderStatus.objects.create(status=status)
            
        except KeyError:
            return JsonResponse({"message": "Key Error!!"}, status=200)
