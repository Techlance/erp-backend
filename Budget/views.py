from django.db import reset_queries
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
# from Company.models import user_company
# from Company.models import user_group
import jwt
from django.http import JsonResponse
from .serializers import *
from Company.models import *
from Users.models import User, transaction_right, user_group, user_right
from datetime import date, timedelta
from django.http.response import HttpResponse
import PIL
import json

# Function to verify token for authorization
def verify_token(request):
    try:
        if not (request.headers['Authorization'] == "null"):
            token = request.headers['Authorization']
    except:
        if not (request.COOKIES.get('token') == "null"):
            token = request.COOKIES.get('token')

    else:
        context = {
            "success":False,
            "message":"INVALID_TOKEN",
            }
        payload = JsonResponse(context)
        
    if not token:
        context = {
                "success":False,
                "message":"INVALID_TOKEN",
            }
        payload =  JsonResponse(context)
    try:
        # Decode Token
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except :
        context = {
                "success":False,
                "message":"INVALID_TOKEN",
            }
        payload =  JsonResponse(context)
    return payload


# function getting error from serializer
def get_error(serializerErr):
    err = ''
    for i in serializerErr:
        err = serializerErr[i][0]
        break    
    return err


# check transaction permission of specific user group in which user is involved
def check_user_company_right(transaction_rights, user_company_id, user_id, need_right):
    try:
        # Query-1 : obtain Transaction Right
        check_transaction_right = transaction_right.objects.filter(transactions=transaction_rights)[0].id
        # Query-2 : Obtain Group id from user company
        check_user_group = user_company.objects.get(user=user_id, company_master_id=user_company_id).user_group_id.id
        # find instance of Query-1 and Query-2
        transaction_right_instance = transaction_right.objects.get(id=check_transaction_right)
        user_group_instance = user_group.objects.get(id=check_user_group)
        # Query-3 : check user right 
        check_user_right = user_right.objects.get(user_group_id=user_group_instance, transaction_id=transaction_right_instance)
        
    except:
        # print('debug')
        return False
    
    # check condition for user permission
    if need_right=="can_create":
        return check_user_right.can_create
    elif need_right=="can_alter":
        return check_user_right.can_alter
    elif need_right=="can_delete":
        return check_user_right.can_delete
    else:
        return check_user_right.can_view

############################################################################################################################
################################################## BUDGET (CUD) #################################################
############################################################################################################################

# API For adding budget
# request : POST
# endpoint : create-budget
class CreateBudget(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission
        user_permission=False
        if request.data['budget_type']=='P&L':
            user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_create")
        elif request.data['budget_type']=='Cashflow':
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_create")

        if user_permission :
            # print(request.data)
            
            serializer = BudgetSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                }
                })
            
            company_name = company_master.objects.get(id=request.data['company_master_id']).company_name
            serializer.save()
            
            
            return Response({
                "success":True,
                "message":"Budget added to "+company_name+" successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to add budget",
            "data": {
                    "email":user.email
                }
            })
        
           



# API For editing budget
# request : PUT
# endpoint : edit-budget/id
class EditBudget(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission
        user_permission=False
        # print(int(request.data['authoriser']),int(user.id))
        if int(request.data['authoriser'])==int(user.id):
            if request.data['budget_type']=='P&L':
                user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_edit")
                
            elif request.data['budget_type']=='Cashflow':
                user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_edit")
        # print(user_permission)
        if user_permission:
            budget_instance = budget.objects.get(id=id)
            serializer = BudgetSerializer(budget_instance, data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            
            serializer.save()
            
            return Response({
                "success":True,
                "message":"Budget has been edited successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to edit Budget",
            "data": {
                    "email":user.email
                }
            })


# API For deleting budget
# request : DELETE
# endpoint : delete-budget/<int:id> 
class DeleteBudget(APIView):
    def delete(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        user_permission=False
        if int(request.data['authoriser'])==int(user.id):
            if request.data['budget_type']=='P&L':
                user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_delete")
            elif request.data['budget_type']=='Cashflow':
                user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_delete")
        
        if user_permission:

            budget_instance = budget.objects.get(id=id)
            b_name = budget_instance.budget_name
            company_name = budget_instance.company_master_id.company_name
            budget_instance.delete()
            return Response({
                'success': True,
                'message': "Budget "+b_name+" for " + company_name + " has been removed",
                })

        else:
            
            return Response({
                'success': False,
                'message': 'You are not allowed to delete this Budget',
                })



############################################################################################################################
################################################## BUDGET DETAILS (CUD) #################################################
############################################################################################################################

# API For adding budget
# request : POST
# endpoint : create-budget-details
class CreateBudgetDetails(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission

        user_permission=False
        user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_create")

        if user_permission :
            serializer = BudgetDetailsSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                }
                })
            revised_serializer = RevisedBudgetDetailsSerializer(data = request.data)
            if not revised_serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                }
                })
            
            company_name = company_master.objects.get(id=request.data['company_master_id']).company_name
            serializer.save()
            revised_serializer.save()
            
            return Response({
                "success":True,
                "message":"Budget details added to "+company_name+" successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to add budget",
            "data": {
                    "email":user.email
                }
            })
        
           



# API For editing budget
# request : PUT
# endpoint : edit-budget-details/id
class EditBudgetDetails(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission
        budget_instance = budget.objects.get(id=request.data['budget_id'])
        user_permission=False
        if budget_instance.authoriser.id==user.id:
            user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_edit")
        
        if user_permission:
            budget_details_instance = budget_details.objects.get(id=id)
            serializer = BudgetDetailsSerializer(budget_details_instance, data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            
            serializer.save()
            
            return Response({
                "success":True,
                "message":"Budget details has been edited successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to edit this budget details",
            "data": {
                    "email":user.email
                }
            })


# API For deleting budget
# request : DELETE
# endpoint : delete-budget-details/<int:id> 
class DeleteBudgetDetails(APIView):  
    def delete(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        budget_instance = budget.objects.get(id=request.data['budget_id'])
        user_permission=False
        if budget_instance.authoriser.id==user.id:
            user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_delete")

        if user_permission:
            budget_details_instance = budget_details.objects.get(id=id)
            revised_budget_details_instance = revised_budget_details.objects.get(id=id)
            budget_instance.delete()
            revised_budget_details_instance.delete()

            return Response({
                'success': True,
                'message': "Budget detail has been removed",
                })

        else:
            
            return Response({
                'success': False,
                'message': 'You are not allowed to delete this Budget Detail',
                })


############################################################################################################################
################################################## REVISED BUDGET DETAILS (U) #################################################
############################################################################################################################


# API For editing budget
# request : PUT
# endpoint : edit-revised-budget-details/id
class EditRevisedBudgetDetails(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission
        revised_budget_instance = revised_budget_details.objects.get(id=id)
        user_permission=False
        if revised_budget_instance.authoriser==user.id:
            user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_edit")
        
        if user_permission:
            revised_budget_details_instance = revised_budget_details.objects.get(id=id)
            serializer = RevisedBudgetDetailsSerializer(revised_budget_details_instance, data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            
            serializer.save()
            
            return Response({
                "success":True,
                "message":"Revised Budget details has been edited successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to edit this revised budget details",
            "data": {
                    "email":user.email
                }
            })


############################################################################################################################
################################################## BUDGET CASHFLOW DETAILS (CUD) #################################################
############################################################################################################################

# API For adding budget cashflow details
# request : POST
# endpoint : create-budget-cashflow-detail
class CreateBudgetCashflowDetails(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission

        user_permission=False
        user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_create")

        if user_permission :
            serializer = BudgetCashflowSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                }
                })
            revised_serializer = RevisedBudgetCashflowSerializer(data = request.data)
            if not revised_serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                }
                })
            
            company_name = company_master.objects.get(id=request.data['company_master_id']).company_name
            serializer.save()
            revised_serializer.save()
            
            return Response({
                "success":True,
                "message":"Budget Cashflow details added to "+company_name+" successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to add budget cashflow",
            "data": {
                    "email":user.email
                }
            })
        
           



# API For editing budget cashflow details
# request : PUT
# endpoint : budget-cashflow-detail/id
class EditBudgetCashflowDetails(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission
        budget_instance = budget.objects.get(id=id)
        user_permission=False
        if budget_instance.authoriser==user.id:
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_edit")
        
        if user_permission:
            budget_cashflow_details_instance = budget_cashflow_details.objects.get(id=id)
            serializer = BudgetCashflowSerializer(budget_cashflow_details_instance, data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            
            serializer.save()
            
            return Response({
                "success":True,
                "message":"Budget Cashflow details has been edited successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to edit this budget Cashflow details",
            "data": {
                    "email":user.email
                }
            })


# API For deleting budget cashflow details
# request : DELETE
# endpoint : delete-budget-cashflow-details/<int:id> 
class DeleteBudgetCashflowDetails(APIView):  
    def delete(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        budget_instance = budget.objects.get(id=id)
        user_permission=False
        if budget_instance.authoriser==user.id:
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_delete")

        if user_permission:
            budget_cashflow_details_instance = budget_cashflow_details.objects.get(id=id)
            revised_budget_details_instance = revised_budget_cashflow_details.objects.get(id=id)
            budget_cashflow_details_instance.delete()
            revised_budget_details_instance.delete()

            return Response({
                'success': True,
                'message': "Budget Cashflow detail has been removed",
                })

        else:
            
            return Response({
                'success': False,
                'message': 'You are not allowed to delete this Budget Cashflow Detail',
                })



############################################################################################################################
################################################## REVISED BUDGET CASHFLOW DETAILS (U) #################################################
############################################################################################################################


# API For editing budget cashflow details
# request : PUT
# endpoint : edit-revised-budget-cashflow-details/id
class EditRevisedBudgetCashflowDetails(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission
        revised_budget_cashflow_instance = revised_budget_cashflow_details.objects.get(id=id)
        user_permission=False
        if revised_budget_cashflow_instance.authoriser==user.id:
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_edit")
        
        if user_permission:
            revised_budget_cashflow_details_instance = revised_budget_cashflow_details.objects.get(id=id)
            serializer = RevisedBudgetCashflowSerializer(revised_budget_cashflow_details_instance, data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            
            serializer.save()
            
            return Response({
                "success":True,
                "message":"Revised Budget Cashflow details has been edited successfully",
                "data": serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to edit this revised budget cashflow details",
            "data": {
                    "email":user.email
                }
            })


# TODO: 1) CHECK ALL VIEWS HERE AND 2) MAKE GET API FOR BUDGET OVERALL