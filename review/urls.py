from django.urls import path
from .views      import ReviewView, ReviewCreateView

urlpatterns = [
    path("/create", ReviewCreateView.as_view()),
    path("/<int:id>", ReviewView.as_view())
]