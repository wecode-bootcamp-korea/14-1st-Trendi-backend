import json

from django.views import View
from django.http import JsonResponse

from .models import Review
from user.models import User
from product.models import Product

class ReviewView(View):
    def post(self, request):
        data=json.loads(request.body)
        print("------request.body", request.body)
        try:
            user             = User.objects.get(pk=data['user_id'])
            product          = Product.objects.get(pk=data["product_id"])
            content          = data["content"].strip()
            image_url        = data.get("image_url")
            user_information = data.get("user_information")
            star             = data["star"]
            print("-----user_information---",user_information)

            Review.objects.create(
                user             = user,
                product          = product,
                content          = content,
                image_url        = image_url,
                star             = star,
                user_information = user_information
            )
            return JsonResponse({"message": "Review Success!!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"This nick_name is not exist!"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"message":"This product is not exist!"}, status=400)
        except KeyError:
            return JsonResponse({"message": "Key Error!!"}, status=400)
        # except Exception as ex:
            # return JsonResponse({"extra error message": f"{ex}"}, status=400)

    def get(self, request, id):
        try:
            product_id = id
            reviews = Review.objects.filter(product=product_id)

            if not reviews.exists():
                return JsonResponse({"message": "There are not any reviews"}, status=200)
            review_list = []
            for review in reviews:
                review_data = {
                    "content"   : review.content,
                    "image_url" : review.image_url,
                    "star"      : review.star,
                    "nick_name" : review.user.nick_name,
                    "product"   : review.product_id,
                    "updated_at": str(review.updated_at),
                    # "user_information": review.user_information
                }
                review_list.append(review_data)
            return JsonResponse({"message": review_list}, status=200)
        except KeyError:
            return JsonResponse({"message": "Key Error!"}, status=400)
        except Exception as ex:
            return JsonResponse({"extra error message": f"{ex}"}, status=400)
    
    def delete(self, request):
        data = json.loads(request.body)

        try:
            user_id   = data["user_id"]
            review_id = data["review_id"]
            review_to_delete = Review.objects.get(pk=review_id)

            if review_to_delete.user_id is not user_id:
                return JsonResponse({"message": "You do not have permission to delete the review"}, status=400)
            review_to_delete.delete()
            return JsonResponse({"message": "delete success!"}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({"message": "review is not exists!"}, status=400)
        except KeyError:
            return JsonResponse({"message": "Key Error!"}, status=400)
        except Exception as ex:
            return JsonResponse({"extra error message": f"{ex}"}, status=400)

    def put(self, request):
        data = json.loads(request.body)

        try:
            user_id          = data["user_id"]
            review_id        = data["review_id"]
            content          = data["content"]
            user_information = data["user_information"]
            image_url        = data["image_url"]
            star             = data["star"]
            review_to_update = Review.objects.get(pk=review_id)

            if review_to_update.user_id is not user_id:
                return JsonResponse({"message": "You do not have permission to update the review"}, status=400)
            review_to_update.content=content
            review_to_update.image_url=image_url
            review_to_update.star=star
            review_to_update.user_information=user_information
            review_to_update.save()
            return JsonResponse({"message": "update success!"}, status=200)            
        except Review.DoesNotExist:
            return JsonResponse({"message": "review is not exists!"}, status=400)
        except KeyError:
            return JsonResponse({"message": "Key Error!"}, status=400)
        except Exception as ex:
            return JsonResponse({"extra error message": f"{ex}"}, status=400)