from django.urls import path
from .views import *

urlpatterns = [
    path('create-budget', CreateBudget.as_view()),
    path('edit-budget/<int:id>', EditBudget.as_view()),  # id : budget id
    path('delete-budget/<int:id>', DeleteBudget.as_view()), # id : budget id
    

    path('get-budget-details/<int:id>', GetBudgetDetails.as_view()), # id: budget id
    path('create-budget-details', CreateBudgetDetails.as_view()),
    path('edit-budget-details/<int:id>', EditBudgetDetails.as_view()), # id : 
    path('edit-changed-budget-details/<int:id>', EditChangedBudgetDetails.as_view()), # id : 
    path('delete-budget-details/<int:id>', DeleteBudgetDetails.as_view()), # id : 
    
    
]
