import json

from django.views     import View
from django.http      import JsonResponse

from user.models import User 

class SearchView(View):
    def get(request):
        data = json.loads(request.body) 
        results = Product.objects.filter(title__contain=data['result'])

        if not results.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)
    
        results = [{
            'title'            : product.title,
            'thumb_image'      : product.thumb_image ,
            'discounted_price' : round(product.price * (1-product.sale),-2),
            'price'            : product.price,
            'seller'           : product.seller.name,
            'delivery'         : product.delivery,
            'sale'             : str(product.sale * 100) + '%'
            } for result in results]
        return JsonResponse({'results': results}, status = 200)