from django.urls import path
from .views import OrderListView, OrderView

urlpatterns = [
    path("/orderlist", OrderListView.as_view()),
    path("/orderlist/<int:id>", OrderListView.as_view()),
    path("/order", OrderView.as_view())

]