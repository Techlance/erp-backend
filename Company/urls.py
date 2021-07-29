from django.urls import path
from .views import GetUserCompanyView


urlpatterns = [
    
    path('get-user-company', GetUserCompanyView.as_view()),
 
]