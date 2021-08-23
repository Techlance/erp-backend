""" 
Developed by Techlace 
updated on : 12-08-2021
Status : {
    "API": done, 
    "backend testing : done, 
    "documentation: done,
    "postman API added" : done,
    }
"""


from django.urls import path
from .views import *

urlpatterns = [
    path('get-ledger-ids-with-bs/<int:id>', GetLedgerIdsWithBs.as_view()), # id =  comapany id
    path('add-ledger-balance', AddLedgerBalance.as_view()),
    path('get-ledger-balance/<int:id>', GetLedgerBalance.as_view()), # id= company id
    path('edit-ledger-balance/<int:id>', EditLedgerBalance.as_view()),
    path('delete-ledger-balance/<int:id>', DeleteLedgerBalance.as_view()),


    path('add-ledger-bal-billwise', AddLedgerBalBillwise.as_view()),
    path('edit-ledger-bal-billwise/<int:id>', EditLedgerBalBillwise.as_view()),
    path('delete-ledger-bal-billwise/<int:id>', DeleteLedgerBalBillwise.as_view()),
    path('get-ledger-bal-billwise/<int:id>', GetLedgerBalBillwise.as_view()),
    path('add-all-ledger-bal-billwise', AddAllLedgerBalBillwise.as_view()),
    path('add-existing-ledger-bal-billwise', AddExistingLedgerBalBillwise.as_view()),


    
    
    path('add-op-bal-brs', AddOpBalBrs.as_view()),
    path('edit-op-bal-brs/<int:id>', EditOpBalBrs.as_view()),
    path('delete-op-bal-brs/<int:id>', DeleteOpBalBrs.as_view()),
    path('get-op-bal-brs/<int:id>', GetOpBalBrs.as_view()),
]

