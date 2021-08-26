from django.urls import path
from .views import *

urlpatterns = [
    path('add-lc', AddLC.as_view()),
    path('edit-lc/<int:id>', EditLC.as_view()),  # id : lc id
    path('delete-lc/<int:id>', DeleteLC.as_view()), # id : delete id
    path('get-lc/<int:id>', GetLC.as_view()), # id : company id
    path('get-detail-lc/<int:id>', GetDetailLC.as_view()), # id : lc id
    path('get-import-lc/<int:id>', GetImportLC.as_view()), # id : company id
    path('get-export-lc/<int:id>', GetExportLC.as_view()), # id : company id

    path('add-lc-document', AddLCDoc.as_view()),
    path('edit-lc-document/<int:id>', EditLcDoc.as_view()), # id : lc document id
    path('delete-lc-document/<int:id>', DeleteLcDoc.as_view()), # id : lc document id
    path('get-lc-document/<int:id>', GetLcDocuments.as_view()),  # id : lc document id
    path('download-lc-document/<int:id>', DownloadLcDoc.as_view()), # id : lc document id

    path('add-lc-amend', AddLCAmend.as_view()),
    path('edit-lc-amend/<int:id>', EditLCAmend.as_view()), # id : lc id
    path('delete-lc-amend/<int:id>', DeleteLCAmend.as_view()), # id : lc id
    path('get-lc-amend/<int:id>', GetLCAmend.as_view()) # id : lc id
    
    
]
