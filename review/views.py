import json

from django.views import View
from django.http import JsonResponse

from .models import Review
from user.models import User
from product.models import Product

class ReviewView(View):
    def post(self, request):
        data=json.loads(request.body)

        try:
            user             = User.objects.get(pk=data['user_id'])
            product          = Product.objects.get(pk=data["product_id"])
            content          = data["content"].strip()
            image_url        = data.get("image_url")
            user_information = data.get("user_information")
            star             = data["star"]

            Review.objects.create(
                user             = user,
                product          = product,
                content          = content,
                image_url        = image_url,
                star             = star,
                user_information = user_information
            )
            return JsonResponse({"message":"SUCCESS"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"message":"INVALID_PRODUCT"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)

    def get(self, request, id):
        product_id = id
        reviews = Review.objects.filter(product=product_id)
        #review_id 추가

        if not reviews.exists():
            return JsonResponse({"message":"INVALID_REVIEW"}, status=200)

        review_list = [{
            "review_id"       : review.id,
            "content"         : review.content,
            "image_url"       : review.image_url,
            "star"            : review.star,
            "nick_name"       : review.user.nick_name,
            "product"         : review.product_id,
            "updated_at"      : str(review.updated_at),
            "user_information": review.user_information
        } for review in reviews[::-1]]
        return JsonResponse({"data": review_list}, status=200)
    
    def delete(self, request, id):
        review_id = id
        user_id = int(request.GET['user_id'])

        try:
            review_to_delete = Review.objects.get(pk=review_id)
            if review_to_delete.user_id is not user_id:
                return JsonResponse({"message":"INVALID_USER"}, status=400)
            review_to_delete.delete()
            return JsonResponse({"message":"SUCCESS"}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({"message":"INVALID_REVIEW"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)

    def patch(self, request,id):
        data = json.loads(request.body)
        review_id = id

        try:
            user_id          = data["user_id"]
            content          = data["content"]
            user_information = data["user_information"]
            image_url        = data["image_url"]
            star             = data["star"]
            review_to_update = Review.objects.get(pk=review_id)

            if review_to_update.user_id is not user_id:
                return JsonResponse({"message":"INVALID_USER"}, status=400)
            review_to_update.content=content
            review_to_update.image_url=image_url
            review_to_update.star=star
            review_to_update.user_information=user_information
            review_to_update.save()
            return JsonResponse({"message":"SUCCESS"}, status=200)            
        except Review.DoesNotExist:
            return JsonResponse({"message":"INVALID_REVIEW"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)
