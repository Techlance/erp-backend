from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import LedgerBalanceSerializer, LedgerBalanceBillwiseSerializer, OpBalanceBrsSerializer
from datetime import date, timedelta
from django.http.response import HttpResponse
from .models import ledger_balance,op_bal_brs,ledger_bal_billwise
from Company.models import ledger_master, user_company, year_master
from Users.models import transaction_right, user_group, user_right, User
import jwt
from decimal import Decimal as D
# Create your views here.
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

class GetLedgerIdsWithBs(APIView):
    def get(self, request, id):
        # verify token for authorization
        # payload = verify_token(request)
        # try:
        #     user = User.objects.filter(id=payload['id']).first()  
        # except:
        #     return payload
    
        ledgers  = []

        all_ledger_master = ledger_master.objects.filter(company_master_id=id)
        for instance in all_ledger_master:
            if instance.acc_group_id.acc_head_id.bs==True:
                ledgers.append({'id':instance.id,'ledger_id':instance.ledger_id})
        
        # ledgers  = []

        # all_ledger_master = ledger_master.objects.filter(acc_group_id.acc_head_id.bs==True,company_master_id=id)
        # for instance in all_ledger_master:
        #     ledgers.append({'id':instance.id,'ledger_id':instance.ledger_id})
        # print(ledgers)
        return Response({
            'success': True,
            'message':'',
            'data':ledgers
        })

# API For adding ledger balance
# request : POST
# endpoint : add-ledger-balance
class AddLedgerBalance(APIView):
    def post(self, request):
        payload = verify_token(request)

        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        # check user permission for Account Head from Transaction
        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            year_master_instance = year_master.objects.get(company_master_id=request.data['company_master_id'], year_no=0)
            request.data.update({"year_id":year_master_instance})
            debit = 0 
            credit = 0
            if request.data['dr'] :
                debit = D(request.data['dr'])
            if request.data['cr'] :
                credit = D(request.data['cr'])
            balance = debit+credit
            request.data.update({"amount":balance})
            fc_rate = str(balance/request.data['fc_amount'])
            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = D(fc_rate)
            request.data.update({"fc_rate": fc_rate})
           

            serializer = LedgerBalanceBillwiseSerializer(data = request.data)

            if not serializer.is_valid():
                return Response({
                "success":False,
                "message": get_error(serializer.errors),
                })

            serializer.save()
            return Response({
                "success":True,
                "message":"Ledger balance added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Add ledegr balance',
            })



# API For getting ledger balance
# request : GET
# endpoint : get-ledger-balance/id(company id)
class GetLedgerBalance(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # id is company id
        # check user permission to get account head 
        user_permission = check_user_company_right("Opening Balance", id, user.id, "can_view")
        if user_permission:
            ledger_balance_instance = ledger_balance.objects.filter(company_master_id=id)
            serializer = LedgerBalanceSerializer(ledger_balance_instance, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Ledger Balance',
                'data': []
            })


# API For editing Ledger Balance
# request : PUT
# endpoint : edit-ledger-balance/<int:id>
class EditLedgerBalance(APIView):
    def put(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        
        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            ledger_balance_instance = ledger_balance.objects.get(id=id)
            request.data.update({"year_id":ledger_balance_instance.year_id})
            debit = 0 
            credit = 0
            if request.data['dr'] :
                debit = D(request.data['dr'])
            if request.data['cr'] :
                credit = D(request.data['cr'])
            balance = debit+credit
            request.data.update({"balance":balance})
            fc_rate = str(balance/request.data['fc_amount'])
            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = D(fc_rate)
            request.data.update({"fc_rate": fc_rate})
            serializer = LedgerBalanceSerializer(ledger_balance_instance, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'ledger balance. Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Add ledger balance',
            })



# API For deleting ledger balance
# request : DELETE
# endpoint : delete-ledger-balance/id(ledger balance id)
class DeleteLedgerBalance(APIView):
    def delete(self, request, id):
        # verify token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        ledger_balance_instance = ledger_balance.objects.get(id=id)
        user_permission = check_user_company_right("Opening Balance", ledger_balance_instance.company_master_id, user.id, "can_delete")
        if user_permission:
            
            ledger_balance_instance.delete()
            return Response({
                'success': True,
                'message': 'Ledger Balance deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to delete Ledger balance',
            })


############################################################################################################################
################################################## Ledger Balance Billwise(CRUD) #####################################################
############################################################################################################################


# API For adding Ledger balance billwise
# request : POST
# endpoint : add-ledger-bal-billwie
class AddBalBillwise(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            debit = 0 
            credit = 0
            if request.data['dr'] :
                debit = D(request.data['dr'])
            if request.data['cr'] :
                credit = D(request.data['cr'])
            balance = debit+credit
            request.data.update({"balance":balance})
            fc_rate = str(balance/request.data['fc_amount'])
            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = D(fc_rate)
            request.data.update({"fc_rate": fc_rate})
            serializer = LedgerBalanceBillwiseSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'ledger balance billwise added successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Add ledger balance billwise',
            })


        
# API For editing Ledger Balance Billwise
# request : PUT
# endpoint : edit-ledger-bal-billwise/<int:id>
class EditLedgerBalBillwise(APIView):
    def put(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        
        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            ledger_balance_billwise_instance = ledger_bal_billwise.objects.get(id=id)
            debit = 0 
            credit = 0
            if request.data['dr'] :
                debit = D(request.data['dr'])
            if request.data['cr'] :
                credit = D(request.data['cr'])
            balance = debit+credit
            request.data.update({"balance":balance})
            fc_rate = str(balance/request.data['fc_amount'])
            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = D(fc_rate)
            request.data.update({"fc_rate": fc_rate})
            serializer = LedgerBalanceBillwiseSerializer(ledger_balance_billwise_instance, data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'ledger balance billwise edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit ledger balance billwise',
            })


# API For deleting ledger balance billwise
# request : DELETE
# endpoint : delete-ledger-bal-billwise/id (ledger balance billwise id)
class DeleteLedgerBalBillwise(APIView):
    def delete(self, request, id):
        # verify token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        ledger_balance_billwise_instance = ledger_bal_billwise.objects.get(id=id)
        user_permission = check_user_company_right("Opening Balance", ledger_balance_billwise_instance.company_master_id, user.id, "can_delete")
        if user_permission:
            ledger_balance_billwise_instance.delete()
            return Response({
                'success': True,
                'message': 'Ledger Balance Billwie deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to delete Ledger balance Billwise',
            })


# API For getting ledger balance billwise
# request : GET
# endpoint : get-ledger-bal-billwise/id (company id)
class GetLedgerBalance(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission = check_user_company_right("Opening Balance", id, user.id, "can_view")
        if user_permission:
            ledger_balance_instance = ledger_bal_billwise.objects.filter(company_master_id=id)
            serializer = LedgerBalanceBillwiseSerializer(ledger_balance_instance, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Ledger Balance',
                'data': []
            })


############################################################################################################################
################################################## OP Balance BRS(CRUD) #####################################################
############################################################################################################################


# API For adding op balance brs
# request : POST
# endpoint : add-op-bal-brs
class AddOpBalBrs(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            year_master_instance = year_master.objects.get(company_master_id=request.data['company_master_id'], year_no=1)
            request.data.update({"year_id":year_master_instance})

            serializer = OpBalanceBrsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'op bal brs added successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to add op balance brs',
            })


# API For editing Op balance brs
# request : PUT
# endpoint : edit-op-bal-brsse/<int:id>
class EditOpBalBrs(APIView):
    def put(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        
        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            op_bal_brs_instance = op_bal_brs.objects.get(id=id)
            request.data.update({"year_id":op_bal_brs_instance.year_id})
            serializer = OpBalanceBrsSerializer(op_bal_brs_instance, data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'op bal brs edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit op balance brs',
            })


# API For deleting op balance brs
# request : DELETE
# endpoint : delete-op-bal-brs/id (ledger balance billwise id)
class DeleteOpBalBrs(APIView):
    def delete(self, request, id):
        # verify token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        op_bal_brs_instance = op_bal_brs.objects.get(id=id)
        user_permission = check_user_company_right("Opening Balance", op_bal_brs_instance.company_master_id, user.id, "can_delete")
        if user_permission:
            op_bal_brs_instance.delete()
            return Response({
                'success': True,
                'message': 'op Balance brs deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to delete op balance brs',
            })


# API For getting op balance brs
# request : GET
# endpoint : get-op-bal-brs/id (company id)
class GetOpBalBrs(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission = check_user_company_right("Opening Balance", id, user.id, "can_view")
        if user_permission:
            op_bal_brs_instance = op_bal_brs.objects.filter(company_master_id=id)
            serializer = LedgerBalanceBillwiseSerializer(op_bal_brs_instance, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Op balance brs',
                'data': []
            })
