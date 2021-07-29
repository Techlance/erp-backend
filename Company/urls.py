from django.urls import path
from .views import CreateCompanyView, DeleteCompanyView, DetailCompanyView, EditCompanyView, GetUserCompanyView


urlpatterns = [
    path('get-user-company', GetUserCompanyView.as_view()),
    path('create-company', CreateCompanyView.as_view()),
    path('edit-company/<int:id>', EditCompanyView.as_view()),
    path('delete-company/<int:id>', DeleteCompanyView.as_view()),
    path('view-company/<int:id>', DetailCompanyView.as_view())
 ]