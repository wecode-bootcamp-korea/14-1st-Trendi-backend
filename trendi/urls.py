from django.urls import path, include

urlpatterns = [
    path('review', include('review.urls')),
    path('product', include('product.urls')),
    path('order', include('order.urls'))
]
