from django.urls import path

from .views      import ProductFavorView, SellerFavorView
urlpatterns = [
    path('/product', ProductFavorView.as_view()),
    path('/seller', SellerFavorView.as_view()),
]
