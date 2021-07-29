from django.urls import path
from .views import AddUserView, GetUserView, LoginView, LogoutView, EditUserView, DeleteUserView, DetailUserView


urlpatterns = [
    
    path('add-user', AddUserView.as_view()),
    path('edit-user/<int:id>', EditUserView.as_view()),
    path('delete-user/<int:id>', DeleteUserView.as_view()),
    path('get-users', GetUserView.as_view()),
    path('get-users/<int:id>', DetailUserView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

]