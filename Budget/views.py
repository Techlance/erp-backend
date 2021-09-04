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
from decimal import Decimal as D
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

        # ledger_queryset = ledger_master.objects.all().select_related('acc_group_id').select_related('acc_head_id').filter(bs=True)
        # print(ledger_queryset)

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
            if request.data['budget_type']=='P&L':
                ledgers  = []

                all_ledger_master = ledger_master.objects.filter(company_master_id=request.data['company_master_id'])
                for instance in all_ledger_master:
                    if instance.acc_group_id.acc_head_id.bs==False:
                        ledgers.append({'id':instance.id,'ledger_id':instance.ledger_id})
                # print(ledgers)

                latest_budget = budget.objects.latest('id')
                # print(latest_budget)
                for i in ledgers:
                    new_budget_details = budget_details(budget_id_id=latest_budget.id,company_master_id_id=latest_budget.company_master_id.id,ledger_id_id = i['id'],
                    jan=0,feb=0,mar=0,apr=0,may=0,jun=0,jul=0,aug=0,sep=0,octo=0,nov=0,dec=0,created_by=user.email)
                    new_budget_details.save()
                    new_rev_budget_details = revised_budget_details(budget_id_id=latest_budget.id,company_master_id_id=latest_budget.company_master_id.id,ledger_id_id = i['id'],
                    jan=0,feb=0,mar=0,apr=0,may=0,jun=0,jul=0,aug=0,sep=0,octo=0,nov=0,dec=0,created_by=user.email)
                    new_rev_budget_details.save()

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


# API For getting budget
# request : GET
# endpoint : get-budget/<int:id> 
class GetBudget(APIView):
    def get(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission = check_user_company_right("Budget-P&L", id, user.id, "can_view")
        if user_permission:
            budget_instance = budget.objects.filter(company_master_id=id)
            serializer = GetBudgetSerializer(budget_instance, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Budget',
                'data': []
            })
            


############################################################################################################################
################################################## BUDGET DETAILS (CRUD) #################################################
############################################################################################################################


# API For getting budget details for a budget id
# request : GET
# endpoint : get-budget-details/id (budget id)
class GetBudgetDetails(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission=False
        company_id=budget.objects.get(id=id).company_master_id.id
        user_permission = check_user_company_right("Budget-P&L", company_id, user.id, "can_view")

        if user_permission:
            budget_instance = budget.objects.get(id=id)
            budget_serializer = GetBudgetSerializer(budget_instance)   

            budget_details_instances = budget_details.objects.filter(budget_id=id)
            serializer = GetBudgetDetailsSerializer(budget_details_instances, many=True)

            return Response({
            'success': True,
            'message':'',
            'budget':budget_serializer.data,
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Budget details',
                'data': []
            })


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

        user_permission = check_user_company_right("Budget-P&L", request.data['company_master_id'], user.id, "can_create")
        # print(user_permission)
        # print(request.data['company_master_id'],user.id)
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
                "message":(serializer.errors),
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
        budget_instance = budget.objects.get(id=id)
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

# API For editing all changed budget
# request : PUT
# endpoint : edit-changed-budget-details/id
class EditChangedBudgetDetails(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission
        budget_instance = budget.objects.get(id=id)
        company_id=budget_instance.company_master_id
        user_permission=False
        if budget_instance.authoriser.id==user.id:
            user_permission = check_user_company_right("Budget-P&L", company_id, user.id, "can_edit")
        
        if user_permission:
            changed_budget_details=request.data['changed_budget_details']
            save_instances_budget=[]
            save_instances_revised=[]
            return_data=[]
            for i in changed_budget_details:
                budget_details_instance = budget_details.objects.get(id=i.get('id'))
                revised_budget_details_instance = revised_budget_details.objects.get(id=i.get('id'))
                changed_budget_details_instance=budget_details.objects.filter(id=i.get('id')).values()[0]
                changed_revised_budget_details_instance=revised_budget_details.objects.filter(id=i.get('id')).values()[0]
                # print(budget_details_instance)
                
                # print(changed_budget_details_instance)
                for key,val in i.items():
                    if key!='id':
                        changed_budget_details_instance[key]=D(val)
                        changed_revised_budget_details_instance[key]=D(val)

                changed_budget_details_instance['budget_id']=changed_budget_details_instance['budget_id_id']
                del changed_budget_details_instance['budget_id_id']
                changed_budget_details_instance['company_master_id']=changed_budget_details_instance['company_master_id_id']
                del changed_budget_details_instance['company_master_id_id']
                changed_budget_details_instance['ledger_id']=changed_budget_details_instance['ledger_id_id']
                del changed_budget_details_instance['ledger_id_id']

                changed_revised_budget_details_instance['budget_id']=changed_revised_budget_details_instance['budget_id_id']
                del changed_revised_budget_details_instance['budget_id_id']
                changed_revised_budget_details_instance['company_master_id']=changed_revised_budget_details_instance['company_master_id_id']
                del changed_revised_budget_details_instance['company_master_id_id']
                changed_revised_budget_details_instance['ledger_id']=changed_revised_budget_details_instance['ledger_id_id']
                del changed_revised_budget_details_instance['ledger_id_id']
                
                del changed_revised_budget_details_instance['id']
                del changed_revised_budget_details_instance['created_on']
                del changed_budget_details_instance['id']
                del changed_budget_details_instance['created_on']

                # print(changed_budget_details_instance)
                budget_details_serializer = BudgetDetailsSerializer(budget_details_instance, data = changed_budget_details_instance)
                revised_budget_details_serializer = RevisedBudgetDetailsSerializer(revised_budget_details_instance, data = changed_revised_budget_details_instance)
                # print(budget_details_serializer)
                if not budget_details_serializer.is_valid():
                    return Response({
                    "success":False,
                    "message":budget_details_serializer.errors,
                    "data": {
                        "email":user.email
                    } 
                    })
                if not revised_budget_details_serializer.is_valid():
                    return Response({
                    "success":False,
                    "message":get_error(revised_budget_details_serializer.errors),
                    "data": {
                        "email":user.email
                    } 
                    })
                save_instances_budget.append(budget_details_serializer)
                
                save_instances_revised.append(revised_budget_details_serializer)
            
            for i in save_instances_budget:
                i.save()
                return_data.append(i.data)
            for i in save_instances_revised:
                i.save()
                
            return Response({
                "success":True,
                "message":"Budget details has been edited successfully",
                "data": return_data
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
        budget_details_instance = budget_details.objects.get(id=id)
        budget_instance = budget.objects.get(id=budget_details_instance.budget_id.id)
        user_permission=False
        if budget_instance.authoriser.id==user.id:
            user_permission = check_user_company_right("Budget-P&L", budget_details_instance.company_master_id.id, user.id, "can_delete")

        if user_permission:
            
            revised_budget_details_instance = revised_budget_details.objects.get(id=id)
            budget_details_instance.delete()
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
################################################## REVISED BUDGET DETAILS (RU) #################################################
############################################################################################################################

# API For getting revised budget details for a budget id
# request : GET
# endpoint : get-revised-budget-details/id (budget id)
class GetRevisedBudgetDetails(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission=False
        company_id=budget.objects.get(id=id).company_master_id.id
        user_permission = check_user_company_right("Budget-P&L", company_id, user.id, "can_view")

        if user_permission:
            budget_instance = budget.objects.get(id=id)
            budget_serializer = GetBudgetSerializer(budget_instance)   

            rev_budget_details_instances = revised_budget_details.objects.filter(budget_id=id)
            serializer = RevisedBudgetDetailsSerializer(rev_budget_details_instances, many=True)

            return Response({
            'success': True,
            'message':'',
            'budget':budget_serializer.data,
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Revised Budget details',
                'data': []
            })


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
        budget_instance = budget.objects.get(id=id)
        company_id=budget_instance.company_master_id.id
        user_permission=False
        if budget_instance.authoriser.id==user.id:
            user_permission = check_user_company_right("Budget-P&L", company_id, user.id, "can_edit")
        
        if user_permission:
            changed_budget_details=request.data['changed_budget_details']
            save_instances_budget=[]
            save_instances_revised=[]
            return_data=[]
            for i in changed_budget_details:
                revised_budget_details_instance = revised_budget_details.objects.get(id=i.get('id'))
                # print(revised_budget_details_instance)
                changed_revised_budget_details_instance=revised_budget_details.objects.filter(id=i.get('id')).values()[0]
                # print(budget_details_instance)
                
                # print(changed_budget_details_instance)
                for key,val in i.items():
                    if key!='id':
                        changed_revised_budget_details_instance[key]=D(val)

                
                changed_revised_budget_details_instance['budget_id']=changed_revised_budget_details_instance['budget_id_id']
                del changed_revised_budget_details_instance['budget_id_id']
                changed_revised_budget_details_instance['company_master_id']=changed_revised_budget_details_instance['company_master_id_id']
                del changed_revised_budget_details_instance['company_master_id_id']
                changed_revised_budget_details_instance['ledger_id']=changed_revised_budget_details_instance['ledger_id_id']
                del changed_revised_budget_details_instance['ledger_id_id']
                
                del changed_revised_budget_details_instance['id']
                del changed_revised_budget_details_instance['created_on']
               

                revised_budget_details_serializer = RevisedBudgetDetailsSerializer(revised_budget_details_instance, data = changed_revised_budget_details_instance)
                if not revised_budget_details_serializer.is_valid():
                    return Response({
                    "success":False,
                    "message":get_error(revised_budget_details_serializer.errors),
                    "data": {
                        "email":user.email
                    } 
                    })
                
                
                save_instances_revised.append(revised_budget_details_serializer)
            
                
            for i in save_instances_revised:
                i.save()
                return_data.append(i.data)
                
            return Response({
                "success":True,
                "message":"Revised Budget details has been edited successfully",
                "data": return_data
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

def EditBudgetChilds(changed_data,budget_parent,revised,user):
    save_instances_budget=[]
    save_instances_revised=[]
    return_data=[]

    for i in changed_data:
        if i.get('id')==None:
            serializer = BudgetCashflowSerializer(data = i)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                }
                }) 
            revised_serializer = RevisedBudgetCashflowSerializer(data = i)
            if not revised_serializer.is_valid():
                return Response({
                "success":False,
                "message":(revised_serializer.errors),
                "data": {
                    "email":user.email
                }
                })
            save_instances_budget.append(serializer)
            save_instances_revised.append(revised_serializer)
        else:
            parent_instance = budget_parent.objects.get(id=i.get('id'))
            revised_instance = revised.objects.get(id=i.get('id'))
            changed_parent_instance = budget_parent.objects.filter(id=i.get('id')).values()[0]
            changed_revised_instance = revised.objects.filter(id=i.get('id')).values()[0]

            for key,val in i.items():
                if key!='id':
                    changed_parent_instance[key]=D(val)
                    changed_revised_instance[key]=D(val)
            changed_parent_instance['budget_id']=changed_parent_instance['budget_id_id']
            del changed_parent_instance['budget_id_id']
            changed_parent_instance['company_master_id']=changed_parent_instance['company_master_id_id']
            del changed_parent_instance['company_master_id_id']
            changed_parent_instance['cashflow_head']=changed_parent_instance['cashflow_head_id']
            del changed_parent_instance['cashflow_head_id']

            changed_revised_instance['budget_id']=changed_revised_instance['budget_id_id']
            del changed_revised_instance['budget_id_id']
            changed_revised_instance['company_master_id']=changed_revised_instance['company_master_id_id']
            del changed_revised_instance['company_master_id_id']
            changed_revised_instance['cashflow_head']=changed_revised_instance['cashflow_head_id']
            del changed_revised_instance['cashflow_head_id']
            
            del changed_revised_instance['id']
            del changed_revised_instance['created_on']
            del changed_parent_instance['id']
            del changed_parent_instance['created_on']

            # print(changed_budget_details_instance)

            parent_serializer = BudgetCashflowSerializer(parent_instance, data = changed_parent_instance)
            revised_serializer = RevisedBudgetCashflowSerializer(revised_instance, data = changed_revised_instance)
            # print(budget_details_serializer)
            if not parent_serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(parent_serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            if not revised_serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(revised_serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            save_instances_budget.append(parent_serializer)
            
            save_instances_revised.append(revised_serializer)
        
    for i in save_instances_budget:
        i.save()
        return_data.append(i.data)
    for i in save_instances_revised:
        i.save()
    return Response({
        "success":True,
        "message":"Budget Cashflow details has been updated successfully",
        "data": return_data
        })                 


# API For getting budget cashflow details for a budget id
# request : GET
# endpoint : get-budget-cashflow-details/id (budget id)
class GetBudgetCashflowDetails(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission=False
        company_id=budget.objects.get(id=id).company_master_id.id
        user_permission = check_user_company_right("Budget-Cash flow", company_id, user.id, "can_view")

        if user_permission:
            budget_cashflow_details_instances = budget_cashflow_details.objects.filter(budget_id=id)
            serializer = BudgetCashflowSerializer(budget_cashflow_details_instances, many=True)
            budget_instance = budget.objects.get(id=id)
            budget_serializer = GetBudgetSerializer(budget_instance)  
            return Response({
            'success': True,
            'message':'',
            'budget':budget_serializer.data,
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Budget Cashflow details',
                'data': []
            })


# API For adding budget cashflow details
# request : POST
# endpoint : create-edit-budget-cashflow-detail
class CreateEditBudgetCashflowDetails(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission

        user_permission=False
        creating=False
        for i in request.data['changed_budget_details']:
            if i.get('id')==None:
                creating=True
                break
        if creating:
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_create")
        else:
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_edit")
        # budget_cashflow_details
        if user_permission :
            return EditBudgetChilds(changed_data=request.data['changed_budget_details'],budget_parent=budget_cashflow_details,revised=revised_budget_cashflow_details,user=user)
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

def EditRevisedBudgetChilds(changed_data,revised,user):
    save_instances_budget=[]
    save_instances_revised=[]
    return_data=[]

    for i in changed_data:
        if i.get('id')==None:

            revised_serializer = RevisedBudgetCashflowSerializer(data = i)
            if not revised_serializer.is_valid():
                return Response({
                "success":False,
                "message":(revised_serializer.errors),
                "data": {
                    "email":user.email
                }
                })
            save_instances_revised.append(revised_serializer)
        else:
            
            revised_instance = revised.objects.get(id=i.get('id'))
            changed_revised_instance = revised.objects.filter(id=i.get('id')).values()[0]

            for key,val in i.items():
                if key!='id':
                    changed_revised_instance[key]=D(val)

            changed_revised_instance['budget_id']=changed_revised_instance['budget_id_id']
            del changed_revised_instance['budget_id_id']
            changed_revised_instance['company_master_id']=changed_revised_instance['company_master_id_id']
            del changed_revised_instance['company_master_id_id']
            changed_revised_instance['cashflow_head']=changed_revised_instance['cashflow_head_id']
            del changed_revised_instance['cashflow_head_id']
            
            del changed_revised_instance['id']
            del changed_revised_instance['created_on']

            revised_serializer = RevisedBudgetCashflowSerializer(revised_instance, data = changed_revised_instance)
            # print(budget_details_serializer)

            if not revised_serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(revised_serializer.errors),
                "data": {
                    "email":user.email
                } 
                })
            
            save_instances_revised.append(revised_serializer)
        
    for i in save_instances_revised:
        i.save()
        return_data.append(i.data)

    return Response({
        "success":True,
        "message":"Revised Budget Cashflow details has been updated successfully",
        "data": return_data
        })      
# API For adding revised budget cashflow details
# request : POST
# endpoint : create-edit-revised-budget-cashflow-detail
class CreateEditRevisedBudgetCashflowDetails(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # check user permission

        user_permission=False
        creating=False
        for i in request.data['changed_budget_details']:
            if i.get('id')==None:
                creating=True
                break
        if creating:
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_create")
        else:
            user_permission = check_user_company_right("Budget-Cash flow", request.data['company_master_id'], user.id, "can_edit")
        # budget_cashflow_details
        if user_permission :
            return EditRevisedBudgetChilds(changed_data=request.data['changed_budget_details'],revised=revised_budget_cashflow_details,user=user)
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to add revised budget cashflow",
            "data": {
                    "email":user.email
                }
            })

# API For getting revised budget cashflow details for a budget id
# request : GET
# endpoint : get-revised-budget-cashflow-details/id (budget id)
class GetRevisedBudgetCashflowDetails(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission=False
        company_id=budget.objects.get(id=id).company_master_id.id
        user_permission = check_user_company_right("Budget-Cash flow", company_id, user.id, "can_view")

        if user_permission:
            budget_cashflow_details_instances = revised_budget_cashflow_details.objects.filter(budget_id=id)
            serializer = RevisedBudgetCashflowSerializer(budget_cashflow_details_instances, many=True)
            budget_instance = budget.objects.get(id=id)
            budget_serializer = GetBudgetSerializer(budget_instance)  
            return Response({
            'success': True,
            'message':'',
            'budget':budget_serializer.data,
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Revised Budget Cashflow details',
                'data': []
            })


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


############################################################################################################################
################################################## Cashflow Head (CRUD) #################################################
############################################################################################################################


# API For adding cashflow
# request : POST
# endpoint : add-cashflow-head
class AddCashflowHead(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # if user.is_superuser:
            # request.data.update({'altered_by': user.email})
        temp = request.data

        # context = temp.dict()
        context=temp
        context['altered_by'] = user.email
        serializer = CashflowSerializer(data = context)
        if not serializer.is_valid():
            return Response({
            "success":False,
            "message": get_error(serializer.errors),
            "data": {
                "email":user.email
            }
            })

        serializer.save()
        return Response({
            "success":True,
            "message":"Cashflow Head added successfully",
            "data":serializer.data
            })
        # else:
        #     return Response({
        #         "success":False,
        #         "message":"Not authorized to Add currency",
        #         "data":{
        #             "email":user.email
        #         }
        #     })


# API For editing cashflow
# request : PUT
# endpoint : edit-cashflow/<int:id>
class EditCashflowHead(APIView):
    def put(self, request, id):
        # verfiy token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        temp = request.data
        # context = temp.dict()
        context = temp
        context['altered_by'] = user.email
        cashflow_instance = cashflow_heads.objects.get(id=id)
        serializer = CashflowSerializer(cashflow_instance, data=context)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': get_error(serializer.errors),
                })
    
        serializer.save()
        return Response({
            'success': True,
            'message': 'Cashflow Edited successfully'})
        # else:
        #     return Response({
        #         'success': False,
        #         'message': 'You are not allowed to edit Currency',
        #         })


# API For deleting cashflow
# request : DELETE
# endpoint : delete-cashflow/<int:id>
class DeleteCashflowHead(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission : inherited from can edit company
        # if user.is_superuser:
        cashflow_instance = cashflow_heads.objects.get(id=id)
        cashflow_instance.altered_by = user.email
        cashflow_instance.delete()
        return Response({
            'success': True,
            'message': 'Cashflow Head deleted Successfully',
            })
        # else:
        #     return Response({
        #         'success': False,
        #         'message': 'You are not allowed to delete Cashflow Head',
        #         })


# API For getting cashflow
# request : GET
# endpoint : get-cashflow-heads
class GetCashflowHead(APIView):
    def get(self, request):
        # verify token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        all_cashflows = cashflow_heads.objects.all()
        serializer = CashflowSerializer(all_cashflows, many=True)
        return Response({
        'success': True,
        'message':'',
        'data': serializer.data
        })


# TODO: 1) CHECK ALL VIEWS HERE AND 2) MAKE GET API FOR BUDGET OVERALL

    #   "changed_budget_details":[
    #  {
    #          "jan": "100.0000",
    #          "feb": "300.0000",
    #          "mar": "100.0000",
    #          "apr": "100.0000",
    #          "may": "100.0000",
    #          "jun": "100.0000",
    #          "jul": "100.0000",
    #          "aug": "100.0000",
    #          "sep": "100.0000",
    #          "octo": "100.0000",
    #          "nov": "100.0000",
    #          "dec": "100.0000",
    #          "created_by": "jainam@gmail.com",
    #          "budget_id": 5,
    #          "company_master_id": 11,
    #          "cashflow_head": 3,
    #          "budget_type":"payment"
    #      },