import json

from django.views import View
from django.http  import JsonResponse

from user.models    import User, Seller
from product.models import Product
from .models        import ProductFavor, SellerFavor
from core.utils     import login_decorator


class ProductFavorView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user.id
            product_id = data['product_id']
            if ProductFavor.objects.filter(user=user_id, product=product_id).exists():
                ProductFavor.objects.get(user=user_id, product=product_id).delete()
                return JsonResponse({'MESSAGE':'REMOVED'}, status = 200)
            
            ProductFavor(
                user_id    = user_id,
                product_id = data['product_id']
            ).save()
            return JsonResponse({'MESSAGE':'ADDED_TO_FAVOR_PRODUCT'}, status = 201)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'JSON_DECODE_ERROR:{e}'}, status=400)

    @login_decorator
    def get(self, request,):
        user_id = request.user.id
      #  result = request.GET.get(product_id, None)  이거 가라겟겟 공부
        results = ProductFavor.objects.prefetch_related('product').filter(user=user_id)
        
        if not results.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        result_lists = [{ # 역참조 공부 fetch_selected 공부
            'title'            : result.product.title,
            'thumb_image'      : result.product.thumb_image_url,
            'discounted_price' : int(round(float(result.product.price) * float(1-result.product.sale.sale_ratio),-2)),
            'price'            : result.product.price,
            'seller'           : result.product.seller.name,
            'delivery'         : result.product.delivery.delivery_type,
            'sale'             : str(int(result.product.sale.sale_ratio * 100)) + '%'
            } for result in results]
        
        return JsonResponse({'results': result_lists}, status = 200)

# 여기 필터 만들어야함, 최근 찜한순, 인기순, 낮은 가격순

class SellerFavorView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user_id = request.user.id

            if SellerFavor.objects.filter(user=user_id, seller=data['seller_id']).exists():
                SellerFavor.objects.get(user=user_id, seller=data['seller_id']).delete()
                return JsonResponse({'MESSAGE':'REMOVED'}, status = 200)
            
            SellerFavor(
                user_id   = user_id,
                seller_id = data['seller_id']
            ).save()
            return JsonResponse({'MESSAGE':'ADDED_TO_FAVOR_SELLER'}, status = 201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

    @login_decorator
    def get(self, request):
        user_id = request.user.id
        #result = request.GET['result']
        results = SellerFavor.objects.filter(user=user_id)
        
        if not results.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        result_lists = [{
            'name'      : result.seller.name,
            'image_url' : result.seller.image_url,
            'hash_tag'  : '#' + '#'.join(result.seller.hash_tag.split()),
            } for result in results]
        
        return JsonResponse({'results': result_lists}, status = 200)












