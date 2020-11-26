from datetime import datetime, timedelta

from django.db.models import Sum, Q, Count, F
from django.views   import View
from django.http    import JsonResponse

from product.models import Product

class ProductListView(View):
    
    def get(self, request):
        try:
            is_pick       = request.GET.get('trendi-pick', None)
            ranking_by    = request.GET.get('ranking', None)
            is_sale       = request.GET.get('sale', None)
            is_delivery   = request.GET.get('delivery', None)
            # latest        = request.GET.get('latest', None)
            # price         = request.GET.get('price', None)
            category      = request.GET.get('category', None)
            sub_category  = request.GET.get('sub-category', None)
            # review        = request.GET.get('review', None)
            ordering      = request.GET.get('ordering', None)
            
            products = Product.objects.filter(orderlist__order__orderstatus_id=5).\
                select_related('seller', 'delivery', 'sale', 'category', 'sub_category').\
                prefetch_related('orderlist_set', 'review_set').\
                annotate(sum=Sum('orderlist__quantity')).\
                annotate(review_count=Count('review__id')).order_by('-sum')
            
            print(len(products))
            q = Q()
            
            if is_pick:
                q.add(Q(trendi_pick=is_pick), Q.AND)
                print(q)
                
            if is_sale:
                q.add(Q(sale_id__gt=is_sale), Q.AND)
                print(q)
                
            if ranking_by:
                rank_filter = {'day' : 1, 'week' : 7, 'month' : 30}
                date = datetime.today() - timedelta(days=rank_filter[ranking_by])
                q.add(Q(orderlist__updated_at__gt=date), Q.AND)
                print(q)
                
            if category:
                q.add(Q(category=category), Q.AND)
                print(q)
                
            if sub_category:
                q.add(Q(sub_category=sub_category), Q.AND)
                print(q)
                
            if is_delivery:
                q.add(Q(delivery__delivery_type=is_delivery), Q.AND)
                print(q)
                # sort_type = {latest: '-updated_at', price: '-price'}
                # for key, value in sort_type.items():
                #     if key:
                #         products = products.order_by(value)
                #         break
            
            # if review:
            #     print("==========")
            #     products = products.annotate(review=Sum('review__id'))
            
            sort_type = {
                'order'  : '-sum',
                'latest' : '-updated_at',
                'review' : '-review_count',
                'price'  : '-price'
            }
            
            if ordering in sort_type:
                print(ordering)
                print(sort_type[ordering])
                products = products.order_by(sort_type[ordering])
            
            print(len(products))
            
            product_list = [{
                'is_pick'         : product.trendi_pick,
                'image_url'       : product.thumb_image_url,
                'seller_name'     : product.seller.name,
                'title'           : product.title,
                'delivery'        : product.delivery.delivery_type == 1,
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
                'review_count'    : get_review_count(product),
                'category'        : product.category.id,
                'sub_category'    : product.sub_category.id
            } for product in products.filter(q)]
            
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
    if product.pk == 50:
        print(reviews.count())
    
    return reviews.count()

class SearchView(View):
    def get(self, request):
        keyword = request.GET['keyword']
        products = Product.objects.filter(title__contains=keyword)
        
        if not products.exists():
            return JsonResponse({'MESSAGE' : 'NO_RESULT!'}, status = 400)
        
        product_lists = [{
            'title'            : product.title,
            'thumb_image'      : product.thumb_image_url,
            'discounted_price' : int(round(float(product.price) * float(1-product.sale.sale_ratio),-2)),
            'price'            : product.price,
            'seller'           : product.seller.name,
            'delivery'         : product.delivery.delivery_type,
            'sale'             : str(int(product.sale.sale_ratio * 100)) + '%'
            } for product in products]
        
        number_of_products = Product.objects.filter(title__contains=keyword).count()
        
        return JsonResponse({'number of products': number_of_products, 'products':
            product_lists}, status = 200)
