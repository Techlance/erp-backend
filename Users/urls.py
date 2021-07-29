from django.urls import path
from .views import AddUserView, LoginView, LogoutView


urlpatterns = [
    
    path('add-user/<int:id>', AddUserView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

]