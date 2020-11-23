from datetime import datetime, timedelta
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
            
            if not isinstance(category_num, int) or \
                not isinstance(sub_category_num, int):
                raise TypeError
            
            orders = Order.objects.prefetch_related('orderlist_set') \
                .filter(status=5).order_by('-updated_at')
            
            sold_product_ids = {}
            for order in orders:
                for order_list in order.orderlist_set.all():
                    if not order_list.product_id in sold_product_ids:
                        sold_product_ids[order_list.product_id] = 0
                    sold_product_ids[order_list.product_id] += 1
            
            sold_product_ids = dict(
                sorted(sold_product_ids.items(),
                key     = operator.itemgetter(1),
                reverse = True)
            )
            
            sold_products = [[
                    Product.objects.get(id=sold_product_id),
                    sold_count
            ] for sold_product_id, sold_count in sold_product_ids.items()]
            
            products = []
            for product in sold_products:
                if category_num and sub_category_num:
                    if product[0].category_id == category_num and \
                        product[0].sub_category_id == sub_category_num:
                        products.append(product)
                
                elif category_num and not sub_category_num:
                    if product[0].category_id == category_num:
                        products.append(product)
            
            product_list = [{
                'image_url'       : products[i][0].thumb_image_url,
                'seller_name'     : products[i][0].seller.name,
                'title'           : products[i][0].title,
                'delivery'        : products[i][0].delivery.delivery_type != 0,
                'sale'            : convert_sale(
                                        products[i][0].sale.sale_ratio
                                    ),
                'discounted_price': get_discounted_price(
                                        products[i][0].price,
                                        products[i][0].sale.sale_ratio
                                    ),
                'price'           : products[i][0].price,
                'product_favor'   : products[i][0].productfavor_set.all().count(),
                'updated_date'    : products[i][0].updated_at,
                'product_pk'      : products[i][0].pk,
                'ordered_count'   : products[i][1],
                'review_count'    : get_review_count(products[i][0])
            } for i in range(len(products))]
        
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_PRODUCT"}, status=400)
        
        return JsonResponse({"product_list": product_list}, status=200)

class ProductDetailView(View):
    
    def get(self, request, product_id):
        
        try:
            if not isinstance(product_id, int):
                raise TypeError
            
            product = Product.objects.get(id=product_id)
            
            product_detail_images = product.productdetailimage_set.all()
            
            detail_images = [
                images.detail_image_url for images in product_detail_images
            ]
            
            reviews = product.review_set.all()
            avg_review_point = round(
                sum([review.star for review in reviews]) / reviews.count()
            )
            
            colors  = [color.color.name
                       for color in product.productcolor_set.all()]
            sizes   = [size.size.name
                       for size in product.productsize_set.all()]
            
            product_detail = {
                'image_url'          : product.thumb_image_url,
                'detail_image_list'  : detail_images,
                'seller_name'        : product.seller.name,
                'title'              : product.title,
                'sale'               : convert_sale(product.sale.sale_ratio),
                'price'              : product.price,
                'discounted_price'   : get_discounted_price(
                                            product.price,
                                            product.sale.sale_ratio
                                       ),
                'total_review_count' : reviews.count(),
                'review_avg'         : avg_review_point,
                'color_list'         : colors,
                'size_list'          : sizes,
                'delivery'           : product.delivery.delivery_type != 0,
                'description'        : product.description,
                'product_pk'         : product.pk,
                'review_info'        : [{
                    'star'             : review.star,
                    'user_name'        : review.user.user_name,
                    'updated_at'       : review.updated_at,
                    'user_information' : review.user_information,
                    'content'          : review.content,
                    'product_pk'       : review.product.pk,
                    'review_pk'        : review.pk,
                } for review in reviews]
            }
        
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_PRODUCT"}, status=400)
        
        return JsonResponse({"product_detail": product_detail}, status=200)

def get_discounted_price(price, sale_ratio):
    return round(int(price * (1 - sale_ratio)), -2)

def convert_sale(sale_ratio):
    return int(sale_ratio * 100)

def get_review_count(product):
    reviews = product.review_set.all()
    return reviews.count()