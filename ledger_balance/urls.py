""" 
Developed by Techlace 
updated on : 31-07-2021
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
    path('get-ledger-balance/<int:id>', GetLedgerBalance.as_view()) # id= company id
]