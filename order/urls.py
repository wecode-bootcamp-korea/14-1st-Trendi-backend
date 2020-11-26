from django.urls import path
from .views import OrderListView

urlpatterns = [
    path("/orderlist", OrderListView.as_view()),
    path("/orderlist/<int:id>", OrderListView.as_view())
]