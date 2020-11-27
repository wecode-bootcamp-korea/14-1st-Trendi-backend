from django.urls import path

from .views      import SellerFavorView, ProductFavorView
urlpatterns = [
    path('/seller', SellerFavorView.as_view()),
    path('/product', ProductFavorView.as_view()),

]
