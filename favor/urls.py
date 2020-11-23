from django.urls import path

from .views      import ProductFavorView, SellerFavorView
urlpatterns = [
    path('/product_favor', ProductFavorView.as_view()),
    path('/seller_favor', SellerFavorView.as_view()),
]
