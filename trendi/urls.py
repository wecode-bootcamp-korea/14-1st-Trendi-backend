from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('favor', include('favor.urls')),
    path('product', include('product.urls')),
]

