import json

from django.views import View
from django.http  import JsonResponse

from user.models    import User 
from product.models import Product

class SearchView(View):
    def get(self, request):
        keyword = request.GET['keyword']
        products = Product.objects.filter(title__contains=keyword)
        
        if not products.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

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
        
        return JsonResponse({'number of products': number_of_products,'products': product_lists}, status = 200)
