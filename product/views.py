from datetime         import datetime, timedelta

from django.db.models import Sum, Q, Count, OuterRef, Subquery
from django.views     import View
from django.http      import JsonResponse

from core.utils       import login_decorator
from product.models   import Product
from review.models    import Review
from favor.models     import ProductFavor

class ProductListView(View):

    def get(self, request):
        try:
            search        = request.GET.get('search')
            is_pick       = request.GET.get('trendi-pick')
            ranking_by    = request.GET.get('ranking')
            is_sale       = request.GET.get('sale')
            is_delivery   = request.GET.get('delivery')
            category      = request.GET.get('category')
            sub_category  = request.GET.get('sub-category')
            ordering      = request.GET.get('ordering')
            
            products = Product.objects.\
                filter(orderlist__order__orderstatus_id=5).\
                select_related(
                    'seller',
                    'delivery',
                    'sale',
                    'category',
                    'sub_category'
                ).\
                prefetch_related(
                    'orderlist_set',
                    'review_set'
                ).\
                annotate(sum=Sum('orderlist__quantity')).\
                annotate(review_count=Subquery(
                    Review.objects.filter(product=OuterRef('pk')).values('product').
                        annotate(count=Count('pk')).values('count'))
                )

            q = Q()

            if is_pick:
                q.add(Q(trendi_pick=is_pick), Q.AND)

            if is_sale:
                q.add(Q(sale_id__gt=is_sale), Q.AND)

            if ranking_by:
                rank_filter = {'day' : 1, 'week' : 7, 'month' : 30}
                date = datetime.today() - timedelta(days=rank_filter[ranking_by])
                q.add(Q(orderlist__updated_at__gt=date), Q.AND)

            if category:
                q.add(Q(category=category), Q.AND)

            if sub_category:
                q.add(Q(sub_category=sub_category), Q.AND)

            if is_delivery:
                q.add(Q(delivery__delivery_type=is_delivery), Q.AND)

            sort_type = {
                'latest'  : '-updated_at',
                'review'  : '-review_count',
                'l-price' : 'price',
                'h-price' : '-price',
                None      : '-sum'
            }

            if not ordering:
                products = products.order_by(sort_type[ordering])

            if ordering in sort_type:
                products = products.order_by(sort_type[ordering])

            if search:
                products = Product.objects.select_related(
                    'seller', 'delivery', 'sale',
                )

                q &= Q(title__icontains              = search) |\
                     Q(category__name__icontains     = search) |\
                     Q(sub_category__name__icontains = search) |\
                     Q(seller__name__icontains       = search)
            
            product_list = [
                {
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
                    'updated_date'    : product.updated_at,
                    'product_pk'      : product.pk,
                } for product in products.filter(q)
            ]
            
            number_of_products = products.filter(q).count()

            if not product_list:
                return JsonResponse({"message": "NO_RESULT"}, status=400)

            return JsonResponse(
                {
                    "number_of_products": number_of_products,
                    "product_list"      : product_list,
                }, status=200
            )
        
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_PRODUCT"}, status=400)
        

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

            reviews = product.review_set.all().order_by('-updated_at')

            avg_review_point = round(
                sum([review.star for review in reviews]) / reviews.count()
            )

            colors = [
                color.color.name
                for color in product.productcolor_set.all()
            ]
            
            sizes = [
                size.size.name
                for size in product.productsize_set.all()
            ]
            
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
                'review_info'        : [
                    {
                        'star'             : review.star,
                        'user_name'        : review.user.user_name,
                        'updated_at'       : review.updated_at,
                        'user_information' : review.user_information,
                        'content'          : review.content,
                        'photo_review'     : review.image_url,
                        'product_pk'       : review.product.pk,
                        'review_pk'        : review.pk,
                    } for review in reviews
                ]
            }

            return JsonResponse({"product_detail": product_detail}, status=200)
        
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_PRODUCT"}, status=400)
        

class PrivateProductDetailView(View):
    @login_decorator
    def get(self, request, product_id):
        try:
            if not isinstance(product_id, int):
                raise TypeError

            user    = request.user
            product = Product.objects.get(id=product_id)

            product_detail_images = product.productdetailimage_set.all()

            detail_images = [
                images.detail_image_url for images in product_detail_images
            ]

            reviews = product.review_set.all().order_by('-updated_at')

            avg_review_point = round(
                sum([review.star for review in reviews]) / reviews.count()
            )

            colors = [
                color.color.name
                for color in product.productcolor_set.all()
            ]
            
            sizes = [
                size.size.name
                for size in product.productsize_set.all()
            ]
            
            favor = None
            
            if ProductFavor.objects.filter(user=user.id, product=product).exists():
                favor = ProductFavor.objects.get(
                            user   =user.id,
                            product=product
                        )
            
            product_detail = {
                'image_url'         : product.thumb_image_url,
                'detail_image_list' : detail_images,
                'seller_name'       : product.seller.name,
                'title'             : product.title,
                'sale'              : convert_sale(product.sale.sale_ratio),
                'price'             : product.price,
                'discounted_price'  : get_discounted_price(
                                        product.price,
                                        product.sale.sale_ratio
                                      ),
                'total_review_count': reviews.count(),
                'review_avg'        : avg_review_point,
                'color_list'        : colors,
                'size_list'         : sizes,
                'delivery'          : product.delivery.delivery_type != 0,
                'description'       : product.description,
                'product_pk'        : product.pk,
                'product_favor'     : True if favor.pk else False,
                'review_info'       : [
                    {
                        'star'            : review.star,
                        'user_name'       : review.user.user_name,
                        'updated_at'      : review.updated_at,
                        'user_information': review.user_information,
                        'content'         : review.content,
                        'photo_review'    : review.image_url,
                        'product_pk'      : review.product.pk,
                        'review_pk'       : review.pk,
                    } for review in reviews
                ]
            }
        
            return JsonResponse({"product_detail": product_detail}, status=200)
        
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_PRODUCT"}, status=400)


def get_discounted_price(price, sale_ratio):
    return round(int(price * (1 - sale_ratio)), -2)

def convert_sale(sale_ratio):
    return int(sale_ratio * 100)
