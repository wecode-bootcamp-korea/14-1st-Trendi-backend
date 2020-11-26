from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('review', include('review.urls')),
    path('products', include('product.urls')),
    path('order', include('order.urls')),
    path('favor', include('favor.urls')),
]