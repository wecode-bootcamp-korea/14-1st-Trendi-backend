from django.urls import path
from .views      import SignUpView, LogInView, SignUpIdView, SignUpEmailView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signup-nick-name', SignUpIdView.as_view()),
    path('/signup-email', SignUpEmailView.as_view()),
    path('/login',  LogInView.as_view()),
]
