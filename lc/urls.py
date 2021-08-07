from django.urls import path
from .views import *

urlpatterns = [
    path('add-lc', AddLC.as_view()),


    path('add-lc-amend', AddLCAmend.as_view()),
    path('edit-lc-amend', EditLCAmend.as_view()),
    path('delete-lc-amend', DeleteLCAmend.as_view())
    
]
