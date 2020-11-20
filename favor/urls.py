from django.urls import path

from .views      import ProductFavorView
urlpatterns = [
    path('/wish_product', ProductFavorView.as_view()),
]
