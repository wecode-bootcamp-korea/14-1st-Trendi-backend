from datetime import datetime, timedelta
import operator
from collections import defaultdict
import collections

from django.db.models import Sum, F, Q
from django.views   import View
from django.http    import JsonResponse

from product.models import Product
from order.models import Order

class ProductListView(View):
    
    def get(self, request):
        try:
            # 홈 버튼
            is_pick         = request.GET.get('brandi-pick', None)
            
            # 랭킹 버튼 (기본)
            ranking_by_date = request.GET.get('ranking', None)
            is_sale = request.GET.get('sale', None)
            status = request.GET.get('status', None)
            
            # 랭킹 페이지의 하루 배송 체크박스 + 하루 배송 버튼 클릭
            is_delivery = request.GET.get('delivery', None)
            
            # 하루 배송 정렬 순 order_by (인기순, 최신순, 낮은 가격 순)
            popular = request.GET.get('popular', None)
            latest = request.GET.get('latest', None)
            price = request.GET.get('price', None)
            
            # 쇼핑몰/마켓 * 기본 판매량 순 + category, sub-category
            category = request.GET.get('category', None)
            sub_category = request.GET.get('sub-category', None)
            review = request.GET.get('review', None)
            
            products = Product.objects.select_related(
                'category', 'sub_category', 'seller', 'delivery'
            ).prefetch_related('orderlist_set')
            
            if is_pick:
                print("====brandi_pick")
                products = products.filter(brandi_pick=is_pick)
            
            if ranking_by_date:
                products = products.objects.filter(orderlist__order__status_id=status). \
                    annotate(sum=Sum('orderlist__quantity')).order_by('-sum')
                
                if ranking_by_date == 'day':
                    today = datetime.today().replace(
                        hour        = 0,
                        minute      = 0,
                        second      = 0,
                        microsecond = 0
                    )
                    
                    products = products.filter(orderlist__updated_at__gt=today)
                    print("day=================================")
                    print(len(products))
                    
                if ranking_by_date == 'week':
                    week = datetime.today() - timedelta(days=7)
                    products = products.filter(orderlist__updated_at__gt=week)
                    print("week=================================")
                    print(len(products))
                    
                if ranking_by_date == 'month':
                    month = datetime.today() - timedelta(days=30)
                    products = products.filter(updated_at__gt=month)
                    print("month=================================")
                    print(len(products))
                    
                if is_sale:
                    print("sale=================================")
                    products = products.exclude(sale_id=1)
                    print(len(products))
            
            if is_delivery:
                print("is_delivery================================================")
                products = products.filter(delivery__delivery_type=0)\
                    .annotate(sum=Sum('orderlist__quantity'))
                
                print(len(products))
                
                if popular:
                    print("popular======================================")
                    products = products.order_by('-updated_at')
                    print(len(products))
                
                if latest:
                    print("latest======================================")
                    products = products.order_by('-updated_at')
                    print(len(products))
                
                if price:
                    print("price======================================")
                    products = products.order_by('price')
                    print(len(products))
                
                if is_sale:
                    print("is_sale======================================")
                    products = products.exclude(sale_id=1)
                    print(len(products))
                
                if category:
                    products = products.filter(category=category)
                
                if sub_category:
                    products = products.filter(sub_category=sub_category)
            
            if category:
                products = products.objects.filter(orderlist__order__status_id=status). \
                    annotate(order_count=Sum('orderlist__quantity')). \
                    annotate(review_count=Sum('review_id'))
                
                products.filter(category=category)
                
                if sub_category:
                    products.filter(sub_category=sub_category)
                
                if review:
                    products = products.order_by('-review_count')
            
            product_list = [{
                'is_pick'         : product.brandi_pick,
                'image_url'       : product.thumb_image_url,
                'seller_name'     : product.seller.name,
                'title'           : product.title,
                'delivery'        : product.delivery.delivery_type,
                'sale'            : convert_sale(product.sale.sale_ratio),
                'discounted_price': get_discounted_price(
                                        product.price,
                                        product.sale.sale_ratio
                                    ),
                'price'           : product.price,
                'product_favor'   : product.productfavor_set.all().count(),
                'updated_date'    : product.updated_at,
                'product_pk'      : product.pk,
                'ordered_count'   : product.sum,
                'review_count'    : get_review_count(product)
            } for product in products]
            
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_PRODUCT"}, status=400)
        
        return JsonResponse({"product_list": product_list}, status=200)

class ProductDetailView(View):
    
    def get(self, request, product_id):
        print(product_id)
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


class ProductListTestView(View):

    def get(self, request):
        data = request.GET
        try:
    
            # products = Product.objects.filter(
            #     delivery_id=2, orderlist__order__status_id=5)\
            #     .annotate(sum=Sum('orderlist__quantity'))
    
            # 1. 홈: 브랜디 픽
            # brandi_pick = 1
            # products = Product.objects.filter(brandi_pick=1).order_by('-updated_at')
    
            # 2.랭킹:
    
            # 3. 하루배송
            # delivery_id = 2
            # filter_delivery_id = eval(
            #     "Product.objects.prefetch_related('orderlist_set').filter(delivery_id=2)"
            # )
    
            # 4. 쇼핑몰/마켓
            # brandi_pick
    
            # 4. 쇼핑몰/마켓 - 상위 카테고리, 하위 카테고리
            # products = Product.objects.filter(brandi_pick=1).order_by('-updated_at')
            # products = Product.\
            #     objects.prefetch_related('orderlist_set').\
            #     filter(category_id=2).\
            #     filter(sub_category_id=2)
    
            # 1. 하루 배송 인기순 (판매량 기준)
            # delivery_id = 2, order status = 5
            # products = Product.objects.prefetch_related('orderlist_set').filter(delivery_id=2)
    
            # 판매량을 얻기 위한 고난의 시작...
            # ordered_product_info = []
            # for product in products:
            #     for orderlist in product.orderlist_set.filter(order__status=5):
            #         ordered_product_info.append([orderlist.product_id, orderlist.quantity])
    
            # ordered_products = defaultdict(int)
            # for ordered_product in ordered_product_info:
            #     if not ordered_product[0] in ordered_products:
            #         ordered_products[ordered_product[0]] = ordered_product[1]
            #     ordered_products[ordered_product[0]] += ordered_product[1]
            #
            # sold_product_info = dict(
            #     sorted(ordered_products.items(),
            #            key=operator.itemgetter(1),
            #            reverse=True)
            # )
    
            # products = [
            #     [Product.objects.get(id=sold_product_id), sold_count]
            #     for sold_product_id, sold_count in sold_product_info.items()
            # ]
    
            # product_list = [{
            #     'image_url'       : products[i][0].thumb_image_url,
            #     'seller_name'     : products[i][0].seller.name,
            #     'title'           : products[i][0].title,
            #     'delivery'        : products[i][0].delivery.delivery_type != 0,
            #     'sale'            : convert_sale(
            #         products[i][0].sale.sale_ratio
            #     ),
            #     'discounted_price': get_discounted_price(
            #         products[i][0].price,
            #         products[i][0].sale.sale_ratio
            #     ),
            #     'price'           : products[i][0].price,
            #     'product_favor'   : products[i][0].productfavor_set.all().count(),
            #     'updated_date'    : products[i][0].updated_at,
            #     'product_pk'      : products[i][0].pk,
            #     'ordered_count'   : products[i][1],
            #     'review_count'    : get_review_count(products[i][0])
            # } for i in range(len(products))]
            
            category_num = int(data.get('category', 0))
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
                       key=operator.itemgetter(1),
                       reverse=True)
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

                elif not category_num and sub_category_num:
                    if product[0].sub_category_id == sub_category_num:
                        products.append(product)

            product_list = [{
                'image_url'       : products[i][0].thumb_image_url,
                'seller_name'     : products[i][0].seller.name,
                'title'           : products[i][0].title,
                'delivery'        : products[i][0].delivery.delivery_type != 0,
                'sale'            : convert_sale(
                    products[i][0].sale.sale_ratio
                ),
                'is_sale': products[i][0].sale.sale_ratio != 0,
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