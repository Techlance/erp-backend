from django.urls import path
from .views import *

urlpatterns = [
    path('create-budget', CreateBudget.as_view()),
    path('edit-budget/<int:id>', EditBudget.as_view()),  # id : budget id
    path('delete-budget/<int:id>', DeleteBudget.as_view()), # id : budget id
    path('get-budget/<int:id>', GetBudget.as_view()), # id : company id
    

    path('get-budget-details/<int:id>', GetBudgetDetails.as_view()), # id: budget id
    path('create-budget-details', CreateBudgetDetails.as_view()),
    path('edit-budget-details/<int:id>', EditBudgetDetails.as_view()), # id : budget detail id
    path('edit-changed-budget-details/<int:id>', EditChangedBudgetDetails.as_view()), # id : budget id
    path('delete-budget-details/<int:id>', DeleteBudgetDetails.as_view()), # id : budget detail id

    path('edit-revised-budget-details/<int:id>', EditRevisedBudgetDetails.as_view()), # id : budget id
    path('get-revised-budget-details/<int:id>', GetRevisedBudgetDetails.as_view()), # id : budget id
    
    path('get-cashflow-head/', GetCashflowHead.as_view()),
    path('create-cashflow-head', AddCashflowHead.as_view()),
    path('edit-cashflow-head/<int:id>', EditCashflowHead.as_view()), # id : cashflow head id
    path('delete-cashflow-head/<int:id>', DeleteCashflowHead.as_view()), # id : cashflow head id
    
    path('create-edit-budget-cashflow-detail/', CreateEditBudgetCashflowDetails.as_view()),
    path('get-budget-cashflow-details/<int:id>', GetBudgetCashflowDetails.as_view()),
    
    path('create-edit-revised-budget-cashflow-detail/', CreateEditRevisedBudgetCashflowDetails.as_view()),
    path('get-revised-budget-cashflow-details/<int:id>', GetRevisedBudgetCashflowDetails.as_view()),
    
]
