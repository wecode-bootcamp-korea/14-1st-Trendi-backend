from django.urls import path, include

urlpatterns = [
    path('', include('product.urls')),
    path('review', include('review.urls')),
]