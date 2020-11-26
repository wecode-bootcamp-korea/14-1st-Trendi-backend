import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q


from user.models    import User 
from product.models import Product


class SearchView(View):
    def get(self, request):
        search   = request.GET.get('search')

        products = Product.objects.select_related('seller','delivery','sale')

        search_content = Q()

        if search:
        
        search_content &= 
            Q(title__icontains               = search) |\
            Q(category__name__icontains      = search) |\
            Q(sub_category__name__icontatins = search) |\
            Q(seller__name__icontains        = serach)

        product_lists = [{
            'title'            : product.title,
            'thumb_image'      : product.thumb_image_url,
            'discounted_price' : int(round(float(product.price) * float(1-product.sale.sale_ratio),-2)),
            'price'            : product.price,
            'seller'           : product.seller.name,
            'delivery'         : product.delivery.delivery_type,
            'sale'             : str(int(product.sale.sale_ratio * 100)) + '%'
            } for product in products.filter(search_content)]
        
        number_of_products = products.filter(search_content).count()

        if not product_lists.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        return JsonResponse({'number of results': number_of_products, 'results': product_lists}, status = 200)
