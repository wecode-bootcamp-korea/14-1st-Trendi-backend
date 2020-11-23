from django.urls import path

from .views      import ProductFavorView, SellerFavorView
urlpatterns = [
    path('/product-favor', ProductFavorView.as_view()),
    path('/seller-favor', SellerFavorView.as_view()),
]
