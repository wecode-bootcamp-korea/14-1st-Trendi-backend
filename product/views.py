import json

from django.views     import View
from django.http      import JsonResponse

from user.models    import User 
from product.models import Product

class SearchView(View):
    def get(self, request):
        result = request.GET['result']
        results = Product.objects.filter(title__contains=result)
        
        if not results.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        result_lists = [{
            'title'            : result.title,
            'thumb_image'      : result.thumb_image_url,
            'discounted_price' : int(round(float(result.price) * float(1-result.sale.sale_ratio),-2)),
            'price'            : result.price,
            'seller'           : result.seller.name,
            'delivery'         : result.delivery.delivery_type,
            'sale'             : str(int(result.sale.sale_ratio * 100)) + '%'
            } for result in results]

        number_of_results = Product.objects.filter(title__contains=result).count()
        
        return JsonResponse({'number of results': number_of_results,'results': result_lists}, status = 200)


class SearchView(View): # 셀러들 보여주는 것도 만들어야함,,
    def get(self, request):
        result = request.GET['result']
        results = Product.objects.filter(sub_category=result)
        
        if not results.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        result_lists = [{
            'title'            : result.title,
            'thumb_image'      : result.thumb_image_url,
            'discounted_price' : int(round(float(result.price) * float(1-result.sale.sale_ratio),-2)),
            'price'            : result.price,
            'seller'           : result.seller.name,
            'delivery'         : result.delivery.delivery_type,
            'sale'             : str(int(result.sale.sale_ratio * 100)) + '%'
            } for result in results]

        number_of_results = Product.objects.filter(sub_category=result).count()
        
        return JsonResponse({'number of results': number_of_results,'results': result_lists}, status = 200)