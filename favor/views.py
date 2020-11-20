import json

from django.views     import View
from django.http    import JsonResponse

from user.models import User
from product.models import Product
from .models    import ProductFavor, SellerFavor
from core.utils import login_decorator


class ProductFavorView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id

            if ProductFavor.objects.filter(user=user_id, product=data['product_id']).exists():
                ProductFavor.objects.get(user=user_id, product=data['product_id']).delete()
                return JsonResponse({'MESSAGE':'REMOVED'}, status = 200)
            
            else:
                ProductFavor(
                    user_id    = user_id,
                    product_id = data['product_id']
                ).save()
                return JsonResponse({'MESSAGE':'ADDED_TO_FAVOR_PRODUCT'}, status = 201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

    @login_decorator
    def get(self, request):
        user_id = request.user.id
        favor_products = [ product for product in ProductFavor.objects.filter(user=user_id).values()]
        favor_product  = [ products['product_id'] for products in favor_products]

        product_name        = [Product.objects.get(id=product_id).name for product_id in favor_product]
        product_thumb_image = [Product.objects.get(id=product_id).thumb_image for product_id in favor_product]
        product_price       = [Product.objects.get(id=product_id).price for product_id in favor_product]
       



#class SearchView(View):
#    def get(request):
#        data = json.loads(request.body) 
#        results = Product.objects.filter(title__contain=data['result'])
#
#        if not results.exists():
#            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)
#    
#        results = [{
#            'title'            : product.title,
#            'thumb_image'      : product.thumb_image ,
#            'discounted_price' : round(product.price * (1-product.sale),-2),
#            'price'            : product.price,
#            'seller'           : product.seller.name,
#            'delivery'         : product.delivery,
#            'sale'             : str(product.sale * 100) + '%'
#            } for result in results]
#        return JsonResponse({'results': results}, status = 200)


#class SellerFavorView(View):
