from django.urls import path
from .views import CreateCompanyView, DeleteCompanyView, DetailCompanyView, EditCompanyView, GetUserCompanyView, AddCompanyDocument, DeleteCompanyDocument, EditCompanyDocumentView, GetCompanyDocumentView, GetCurrency, AddCurrency, EditCurrency, DeleteCurrency 


urlpatterns = [
    path('get-user-company', GetUserCompanyView.as_view()),
    path('create-company', CreateCompanyView.as_view()),
    path('edit-company/<int:id>', EditCompanyView.as_view()),
    path('delete-company/<int:id>', DeleteCompanyView.as_view()),
    path('view-company/<int:id>', DetailCompanyView.as_view()),

    path('add-company-document',  AddCompanyDocument.as_view()),
    path('edit-company-document/<int:id>', EditCompanyDocumentView.as_view()), # id : Document id
    path('delete-company-document/<int:id>', DeleteCompanyDocument.as_view()), # id : Document id
    path('get-company-document/<int:id>', GetCompanyDocumentView.as_view()), # id : Company id

    path('add-currency',  AddCurrency.as_view()),
    path('edit-currency/<int:id>', EditCurrency.as_view()), # id : currency id
    path('delete-currency/<int:id>', DeleteCurrency.as_view()), # id : currency id
    path('get-currency', GetCurrency.as_view()), 
 ]