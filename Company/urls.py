from django.urls import path
from .views import CreateCompanyView, GetUserCompanyView


urlpatterns = [
    path('get-user-company', GetUserCompanyView.as_view()),
    path('create-company', CreateCompanyView.as_view())
 ]