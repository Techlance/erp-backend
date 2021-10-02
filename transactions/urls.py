from django.urls import path
from .views import *

urlpatterns = [
    path('get-vouchers', GetVouchers.as_view()), 
]