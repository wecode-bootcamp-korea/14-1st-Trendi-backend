from django.urls import path

from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/trend', ProductListView.as_view(), name='trend'),
    path('/<int:product_id>', ProductDetailView.as_view()),
]