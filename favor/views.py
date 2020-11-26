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
    def get(self, request):
        user_id = request.user.id
        results = ProductFavor.objects.select_related('user','product__seller','product__sale', 'product__delivery').filter(user=user_id)

        if not results.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        result_lists = [{
            'id'               : result.product.id,
            'title'            : result.product.title,
            'thumb_image'      : result.product.thumb_image_url,
            'discounted_price' : int(round(float(result.product.price) * float(1-result.product.sale.sale_ratio),-2)),
            'price'            : result.product.price,
            'seller'           : result.product.seller.name,
            'delivery'         : result.product.delivery.delivery_type,
            'sale'             : str(int(result.product.sale.sale_ratio * 100)) + '%'
            } for result in results]

        number_of_products = ProductFavor.objects.filter(user=user_id).count()

        return JsonResponse({'number of products': number_of_products,'results': result_lists}, status = 200)

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
        results = SellerFavor.objects.select_related('user','seller').filter(user=user_id)
        
        if not results.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        result_lists = [{
            'id'        : result.seller.id,
            'name'      : result.seller.name,
            'image_url' : result.seller.image_url,
            'hash_tag'  : '#' + '#'.join(result.seller.hash_tag.split()),
            } for result in results]
        
        return JsonResponse({'results': result_lists}, status = 200)












