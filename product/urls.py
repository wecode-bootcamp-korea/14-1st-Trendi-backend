from django.urls import path

from product.views import ProductListView, ProductDetailView,PrivateProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/private/<int:product_id>', PrivateProductDetailView.as_view())
]