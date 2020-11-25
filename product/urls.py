from django.urls import path

from product.views import ProductListView, ProductDetailView, ProductListTestView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/products', ProductListTestView.as_view()),
]