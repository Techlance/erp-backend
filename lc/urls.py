from django.urls import path
from .views import *

urlpatterns = [
    path('add-lc', AddLC.as_view()),
    path('edit-lc/<int:id>', EditLC.as_view()),  # id : lc id
    path('delete-lc/<int:id>', DeleteLC.as_view()), # id : delete id
    path('get-lc/<int:id>', GetLC.as_view()), # id : company id



    path('add-lc-amend', AddLCAmend.as_view()),
    path('edit-lc-amend', EditLCAmend.as_view()),
    path('delete-lc-amend', DeleteLCAmend.as_view())
    
]
