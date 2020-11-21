import operator

from django.views   import View
from django.http    import JsonResponse

from product.models import Product
from order.models import Order

class ProductListView(View):
    
    def get(self, request):
        data = request.GET
        
        try:
            category_num     = int(data.get('category', 0))
            sub_category_num = int(data.get('sub-category', 0))
            
            if not type(category_num) is int or not type(sub_category_num) is int:
                raise TypeError
            
            orders = Order.objects.prefetch_related('orderlist_set') \
                .filter(status=5).order_by('-updated_at')
            
            sold_product_ids = {}
            for order in orders:
                for order_list in order.orderlist_set.all():
                    if not order_list.product_id in sold_product_ids:
                        sold_product_ids[order_list.product_id] = 0
                    sold_product_ids[order_list.product_id] += 1
            
            sold_product_ids = dict(sorted(sold_product_ids.items(),
                                           key     = operator.itemgetter(1),
                                           reverse = True))
            
            sold_products = [
                Product.objects.get(id=sold_product_id)
                for sold_product_id in sold_product_ids.keys()
            ]
            
            products = []
            for product in sold_products:
                if category_num and sub_category_num:
                    if product.category_id == category_num and product.sub_category_id == sub_category_num:
                        products.append(product)
                elif category_num and not sub_category_num:
                    if product.category_id == category_num:
                        products.append(product)
            
            result = [{
                'image_url'       : product.thumb_image_url,
                'seller_name'     : product.seller.name,
                'title'           : product.title,
                'delivery'        : product.delivery.delivery_type != 0,
                'sale'            : int(product.sale.sale_ratio * 100),
                'discounted_price': round(int(product.price * (1 - product.sale.sale_ratio)), -2),
                'price'           : product.price,
                'product_favor'   : product.productfavor_set.all().count(),
                'updated_date'    : product.updated_at,
                'product_pk'      : product.pk,
            } for product in products]
        
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_PRODUCT"}, status=400)
        
        return JsonResponse({"get": result}, status=200)