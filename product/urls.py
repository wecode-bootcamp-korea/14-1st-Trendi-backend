from django.urls import path

from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('/trend', ProductListView.as_view(), name='trend'),
    path('products', ProductListView.as_view()),
    path('products/<int:product_id>', ProductDetailView.as_view()),
]