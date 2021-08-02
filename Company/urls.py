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
from .views import AddAccountHead, CreateCompanyView, DeleteAccountHead, DeleteCompanyView, DetailCompanyView, EditAccountHead, EditCompanyView, GetAccountHead, GetUserCompanyView, AddCompanyDocument, DeleteCompanyDocument, EditCompanyDocumentView, GetCompanyDocumentView, GetCurrency, AddCurrency, EditCurrency, DeleteCurrency, AddVoucherType, EditVoucherType, GetVoucherType, DeleteVoucherType, AddCostCategory, EditCostCategory ,DeleteCostCategory ,GetCostCategory,AddAccGroup ,EditAccGroup ,DeleteAccGroup ,GetAccGroup
urlpatterns = [
    path('get-user-company', GetUserCompanyView.as_view()),

    path('create-company', CreateCompanyView.as_view()),  
    path('edit-company/<int:id>', EditCompanyView.as_view()), #id : company id
    path('delete-company/<int:id>', DeleteCompanyView.as_view()), # id : company id
    path('view-company/<int:id>', DetailCompanyView.as_view()), # id : company id

    path('add-company-document',  AddCompanyDocument.as_view()),
    path('edit-company-document/<int:id>', EditCompanyDocumentView.as_view()), # id : Document id
    path('delete-company-document/<int:id>', DeleteCompanyDocument.as_view()), # id : Document id
    path('get-company-document/<int:id>', GetCompanyDocumentView.as_view()), # id : Company id

    path('add-currency',  AddCurrency.as_view()),
    path('edit-currency/<int:id>', EditCurrency.as_view()), # id : currency id
    path('delete-currency/<int:id>', DeleteCurrency.as_view()), # id : currency id
    path('get-currency', GetCurrency.as_view()), 

    path('add-vouchertype', AddVoucherType.as_view()), 
    path('edit-vouchertype/<int:id>', EditVoucherType.as_view()), # id : voucher_type id
    path('delete-vouchertype/<int:id>', DeleteVoucherType.as_view()), # id : voucher_type id
    path('get-vouchertype/<int:id>', GetVoucherType.as_view()), # id company_master_id

    path('add-account-head', AddAccountHead.as_view()),
    path('edit-account-head/<int:id>', EditAccountHead.as_view()), # id : Account head id
    path('delete-account-head/<int:id>', DeleteAccountHead.as_view()), # id : Account head id
    path('get-account-head/<int:id>', GetAccountHead.as_view()), #id : company_master_id

    path('add-cost-category', AddCostCategory.as_view()),
    path('edit-cost-category/<int:id>', EditCostCategory.as_view()), # id : Cost Category id
    path('delete-cost-category/<int:id>', DeleteCostCategory.as_view()), # id : Cost Category id
    path('get-cost-category/<int:id>', GetCostCategory.as_view()), #id : company_master_id

    path('add-account-group', AddAccGroup.as_view()),
    path('edit-account-group/<int:id>', EditAccGroup.as_view()), # id : Account group id
    path('delete-account-group/<int:id>', DeleteAccGroup.as_view()), # id : Account group id
    path('get-account-group/<int:id>', GetAccGroup.as_view()), #id : company_master_id
    
 ]