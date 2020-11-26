from django.urls import path

from product.views import ProductListView, ProductDetailView, SearchView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/search', SearchView.as_view()),
]