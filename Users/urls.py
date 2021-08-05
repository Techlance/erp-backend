from django.urls import path
from .views import AddUserRight, AddUserView, GetUserView, LoginView, LogoutView, EditUserView, DeleteUserView, DetailUserView, AddUserGroup, EditUserGroup, GetUserGroup, DeleteUserGroup, GetUserRight, EditUserRight, DeleteUserRight, VerifyUser


urlpatterns = [
    path('me', VerifyUser.as_view()),
    path('add-user', AddUserView.as_view()),                            # Create
    path('get-users', GetUserView.as_view()),                           # Retrieve
    path('edit-user/<int:id>', EditUserView.as_view()),                 # Update
    path('delete-user/<int:id>', DeleteUserView.as_view()),             # Delete
    path('get-users/<int:id>', DetailUserView.as_view()),               # Retrieve
    
    path('add-user-group', AddUserGroup.as_view()),                     # Create
    path('get-user-group', GetUserGroup.as_view()),                     # Retrieve
    path('edit-user-group/<int:id>', EditUserGroup.as_view()),          # Update
    path('delete-user-group/<int:id>', DeleteUserGroup.as_view()),      # Delete

    path('add-user-right', AddUserRight.as_view()),                     # Create
    path('get-user-right/<int:id>', GetUserRight.as_view()),            # Retrieve (id is user group id)
    path('edit-user-right/<int:id>', EditUserRight.as_view()),          # Update
    path('delete-user-right/<int:id>', DeleteUserRight.as_view()),      # Delete



    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

]