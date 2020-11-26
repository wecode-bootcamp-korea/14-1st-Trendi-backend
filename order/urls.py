from django.urls import path
from .views import OrderListView, OrderListUpdateView

urlpatterns = [
    path("/orderlist", OrderListView.as_view()),
    path("/orderlist/<int:id>", OrderListUpdateView.as_view())
]