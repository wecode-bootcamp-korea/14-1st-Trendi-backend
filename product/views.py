import operator

from django.views   import View
from django.http    import JsonResponse

from product.models import Product, ProductDetailImage
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
                'discounted_price': get_discounted_price(product.price,
                                                         product.sale.sale_ratio),
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


class ProductDetailView(View):
    
    def get(self, request, product_id):
        
        try:
            if not type(product_id) is int:
                raise TypeError
            
            product = Product.objects.get(id=product_id)
            
            product_detail_images = product.productdetailimage_set.filter(product=product)
            
            detail_images = []
            if product_detail_images:
                detail_images = [images.detail_image_url for images in product_detail_images]
            
            reviews = product.review_set.filter(product=product)
            
            review_points_avg = 0
            if reviews:
                total_review_point = 0
                for review in reviews:
                    total_review_point += review.star
                
                review_points_avg = get_avg_review_point(total_review_point, reviews.count())
            
            colors      = product.productcolor_set.filter(product=product)
            color_names = [color.color.name for color in colors]
            sizes       = product.productsize_set.filter(product=product)
            size_name   = [size.size.name for size in sizes]
            
            if product:
                product_detail = {
                    'image_url'          : product.thumb_image_url,
                    'detail_image_list'  : detail_images,
                    'seller_name'        : product.seller.name,
                    'title'              : product.title,
                    'sale'               : int(product.sale.sale_ratio * 100),
                    'price'              : product.price,
                    'discounted_price'   : get_discounted_price(product.price,
                                                                product.sale.sale_ratio),
                    'total_review_count' : reviews.count(),
                    'review_avg'         : review_points_avg,
                    'color_list'         : color_names,
                    'size_list'          : size_name,
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
        
        return JsonResponse({"get": product_detail}, status=200)

def get_discounted_price(price, sale_ratio):
    return round(int(price * (1 - sale_ratio)), -2)

def get_avg_review_point(total_point, total_count):
    return round(total_point / total_count)