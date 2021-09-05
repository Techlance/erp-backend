from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import LedgerBalanceSerializer, LedgerBalanceBillwiseSerializer, OpBalanceBrsSerializer, GetLedgerBalanceSerializer, GetOpBalanceBrsSerializer
from datetime import date, timedelta
from django.http.response import HttpResponse
from .models import ledger_balance,op_bal_brs,ledger_bal_billwise
from Company.models import ledger_master, user_company, year_master, company_master
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
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()  
        except:
            return payload
    
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
            temp = request.data
            context = temp.dict()
            context['year_id'] = year_master_instance.id
            #request.data.update({'year_id':year_master_instance.id})
            debit = 0 
            credit = 0
            if context.get('dr') :
                debit = context.get('dr')
                context['fc_amount'] = request.data['fc_amount']
            if context.get('cr'):
                credit = context.get('cr')
                context['fc_amount'] = (-1)*D(request.data['fc_amount'])
    
            debit = D(debit)
            credit = D(credit)
            balance = debit - credit
            #request.data.update({'balance':balance})
            context['balance'] = balance
            if context['fc_amount'] == 0:
                fc_rate = "0"
            else:
                fc_rate = str(balance/D(context['fc_amount']))
            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = round(D(fc_rate), 4)
            #request.data.update({'fc_rate': fc_rate})
            context['fc_rate'] = fc_rate
            context['total_cr'] = D(credit)
            context['total_dr'] = D(debit)
            serializer = LedgerBalanceSerializer(data = context)

            if not serializer.is_valid():
                return Response({
                "success":False,
                "message": serializer.errors,
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
# endpoint : get-ledger-balance/id(ledger master id)
class GetLedgerBalance(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # id is company id
        # check user permission to get account head 
        ledger_balance_instance = ledger_balance.objects.get(ledger_id=id)
        user_permission = check_user_company_right("Opening Balance", ledger_balance_instance.company_master_id, user.id, "can_view")
        if user_permission:
            
            serializer = GetLedgerBalanceSerializer(ledger_balance_instance)
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
            # request.data.update({"year_id":ledger_balance_instance.year_id})
            temp = request.data
            context = temp.dict()
            context['year_id'] = ledger_balance_instance.year_id.id
            debit = 0 
            credit = 0
            if request.data['dr'] :
                debit = D(request.data['dr'])
                context['fc_amount'] = D(request.data['fc_amount'])
            if request.data['cr'] :
                credit =(-1)*D(request.data['cr'])
                context['fc_amount'] = (-1)*D(request.data['fc_amount'])
            balance = debit+credit
            #request.data.update({"balance":balance})
            context['balance'] = balance
            if context['fc_amount'] == 0:
                fc_rate = "0"
            else:
                fc_rate = str(balance/D(context['fc_amount']))

            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = round(D(fc_rate), 4)
            #request.data.update({"fc_rate": fc_rate})
            context['fc_rate'] = fc_rate
            serializer = LedgerBalanceSerializer(ledger_balance_instance, data=context)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'ledger balance Edited successfully'})
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
            ledger_balance_instance.altered_by = user.email
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
class AddLedgerBalBillwise(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            temp = request.data
            context = temp
            debit = 0 
            credit = 0
            if request.data['dr'] :
                debit = D(request.data['dr'])
            if request.data['cr'] :
                credit = D(request.data['cr'])
            balance = debit+credit
            #request.data.update({"amount":balance})
            context['amount'] = balance
            if D(context['fc_amount']) == 0:
                fc_rate = "0"
            else:
                fc_rate = str(balance/D(context['fc_amount']))
            
            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = round(D(fc_rate), 4)
            #request.data.update({"fc_rate": fc_rate})
            context['fc_rate'] = fc_rate
            serializer = LedgerBalanceBillwiseSerializer(data=context)
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

def update_ledger_balance(id):
    balance = 0
    fc_amt = 0
    ledger_bal_instance = ledger_balance.objects.get(id=id)
    ledger_bal_billwise_instance = ledger_bal_billwise.objects.filter(ledger_bal_id = id)
    for i in ledger_bal_billwise_instance:
        balance += i.amount
        fc_amt += i.fc_amount
    ledger_bal_instance.balance = balance
    if(balance < 0):
        str_bal = str(balance)
        str_bal = str_bal[1:]
        ledger_bal_instance.cr = D(str_bal)
        ledger_bal_instance.dr = 0 
        ledger_bal_instance.total_cr = D(str_bal)
        ledger_bal_instance.total_dr = 0
    else:
        ledger_bal_instance.dr = balance
        ledger_bal_instance.cr = 0 
        ledger_bal_instance.total_dr = balance
        ledger_bal_instance.total_cr = 0
    if fc_amt == 0:
        fc_rate = "0"
    else:
        fc_rate = str(balance/fc_amt)   
        if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
        fc_rate = round(D(fc_rate), 4)
    ledger_bal_instance.fc_rate = fc_rate
    ledger_bal_instance.save()


        
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
            temp = request.data
            context = temp.dict()
            debit = 0 
            credit = 0
            if request.data['dr'] :
                debit = D(request.data['dr'])
            if request.data['cr'] :
                credit = D(request.data['cr'])
            balance = debit-credit
            #request.data.update({"balance":balance})
            context['amount'] = balance
            if D(context['fc_amount']) == 0:
                fc_rate = "0"
            else:
                fc_rate = str(balance/D(context['fc_amount']))
            # fc_rate = str(balance/D(request.data['fc_amount']))
            if fc_rate[0] == "-":
                fc_rate = fc_rate[1:]
            fc_rate = round(D(fc_rate), 4)
            #request.data.update({"fc_rate": fc_rate})
            context['fc_rate'] = fc_rate
            serializer = LedgerBalanceBillwiseSerializer(ledger_balance_billwise_instance, data=context)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            update_ledger_balance(ledger_balance_billwise_instance.ledger_bal_id.id)
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
            update_ledger_balance(ledger_balance_billwise_instance.ledger_bal_id.id)
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
class GetLedgerBalBillwise(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        ledger_balance_billwise_instance = ledger_bal_billwise.objects.filter(ledger_bal_id=id)
        ledger_balance_instance = ledger_balance.objects.get(id=id)
        user_permission = check_user_company_right("Opening Balance", ledger_balance_instance.company_master_id, user.id, "can_view")
        if user_permission:
           
            serializer = LedgerBalanceBillwiseSerializer(ledger_balance_billwise_instance, many=True)
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
            # request.data.update({"year_id":year_master_instance})
            temp = request.data
            context = temp.dict()
            context['year_id'] = year_master_instance.id

            serializer = OpBalanceBrsSerializer(data=context)
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
            # request.data.update({"year_id":op_bal_brs_instance.year_id})
            temp = request.data
            context = temp.dict()
            context['year_id'] = op_bal_brs_instance.year_id.id
            serializer = OpBalanceBrsSerializer(op_bal_brs_instance, data=context)
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
            op_bal_brs_instance.altered_by = user.email
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
            serializer = GetOpBalanceBrsSerializer(op_bal_brs_instance, many=True)
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



# API For getting detail op balance brs
# request : GET
# endpoint : get-detail-op-bal-brs/id (brs id)
class GetDetailOpBalBrs(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        op_bal_brs_instance = op_bal_brs.objects.get(id=id)
        user_permission = check_user_company_right("Opening Balance", op_bal_brs_instance.company_master_id, user.id, "can_view")
        if user_permission:
           
            serializer = GetOpBalanceBrsSerializer(op_bal_brs_instance)
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

    



# new ledger balance
# API For adding Ledger balance billwise together
# request : POST
# endpoint : add-all-ledger-bal-billwise
class AddAllLedgerBalBillwise(APIView):
    def post(self, request):
            payload = verify_token(request)
            try:
                user = User.objects.filter(id=payload['id']).first()
            except:
                return payload

        # user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
        # if user_permission:
            ref_no = []
            for i in request.data['billwise']:
                if i.get('ref_no') in ref_no:
                     return Response({
                            'success': False,
                            'message': 'Refrence Number is not unique',
                        })
                else:
                    ref_no.append(i.get('ref_no'))
            year_id = year_master.objects.get(company_master_id=request.data['company_master_id'], year_no=0).id
            ledger_id = request.data['ledger_master_id']
            try:
            
                ledger_bal_instance = ledger_balance.objects.get(ledger_id=ledger_id)
                
                user_permission_cr = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
                user_permission_al = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_alter")
                if request.data['fc_name']:
                    fc_name = request.data['fc_name']
                else:
                    fc_name = company_master.objects.get(id=request.data['company_master_id']).base_currency.id
                for i in request.data['billwise']:
               
                    if i.get('id'):
                        if user_permission_al:
                            ledger_balance_billwise_instance = ledger_bal_billwise.objects.get(id=i.get('id'))
                            #print(i.get('id'))
                            context = i
                            debit = 0 
                            credit = 0
                            # del context['id']
                            if i.get('dr'):
                                debit = D(i.get('dr'))
                                context['dr'] = D(i.get('dr'))
                                context['cr'] = 0
                            if i.get('cr') :
                                credit = D(i.get('cr'))
                                context['cr'] = D(i.get('cr'))
                                context['dr'] = 0
                            balance = debit-credit
                           
                            context['amount'] = balance
                            context['ledger_bal_id'] = ledger_bal_instance.id
                            context['fc_name'] = fc_name
                            context['company_master_id'] = request.data['company_master_id']
                            context['total_cr'] = context['cr']
                            context['total_dr'] = context['dr']
                            if D(context['fc_amount']) == 0:
                                fc_rate = "0"
                            else:
                                fc_rate = str(balance/D(context['fc_amount']))
                          
                            if fc_rate[0] == "-":
                                fc_rate = fc_rate[1:]
                            fc_rate = round(D(fc_rate), 4)
                            
                            context['fc_rate'] = fc_rate
                            serializer = LedgerBalanceBillwiseSerializer(ledger_balance_billwise_instance, data=context)
                            if not serializer.is_valid():
                                return Response({
                                    'success': False,
                                    'message': get_error(serializer.errors),
                                    })
                            

                        else:
                            return Response({
                            'success': False,
                            'message': 'You are not allowed to edit ledger balance billwise',
                        })
                    else:
                        if user_permission_cr:
                            temp =i
                            temp.update({"fc_name":fc_name})
                            temp.update({"ledger_bal_id": ledger_bal_instance.id})
                            temp.update({"company_master_id":request.data['company_master_id']})
                            if D(i['fc_amount']) == 0:
                                fc_rate = "0"
                            else:
                                fc_rate = str(D(i['amount'])/D(i['fc_amount']))
                            if fc_rate[0] == "-":
                                fc_rate = fc_rate[1:]
                            fc_rate = round(D(fc_rate), 4)
                            temp.update({"fc_rate": fc_rate})
                        

                            if temp['cr'] is None:
                                temp['cr'] = 0                        

                            if temp['dr'] is None:
                                temp['dr'] = 0

                            serializer = LedgerBalanceBillwiseSerializer(data=temp)
                            if not serializer.is_valid():
                                return Response({
                                    'success': False,
                                    'message': get_error(serializer.errors),
                                    })

                        else:
                            return Response({
                            'success': False,
                            'message': 'You are not allowed to Add ledger balance billwise',
                        })
                
                for i in request.data['billwise']:
               
                    if i.get('id'):
                        if user_permission_al:
                            ledger_balance_billwise_instance = ledger_bal_billwise.objects.get(id=i.get('id'))
                            # del context['id']
                            context = i
                            debit = 0 
                            credit = 0
                            #print(i.get('dr'),i.get('cr'))
                            if i.get('dr') != 0:
                                debit = D(i.get('dr'))
                                context['dr'] = D(i.get('dr'))
                                context['cr'] = 0
                            if i.get('cr') != 0:
                                credit = D(i.get('cr'))
                                context['cr'] = D(i.get('cr'))
                                context['dr'] = 0
                            balance = debit-credit
                           
                            context['amount'] = balance
                            context['ledger_bal_id'] = ledger_bal_instance.id
                            context['fc_name'] = fc_name
                            if D(context['fc_amount']) == 0:
                                fc_rate = "0"
                            else:
                                fc_rate = str(balance/D(context['fc_amount']))
                          
                            if fc_rate[0] == "-":
                                fc_rate = fc_rate[1:]
                            fc_rate = round(D(fc_rate), 4)
                            context['company_master_id'] = request.data['company_master_id']
                            context['fc_rate'] = fc_rate
                            serializer = LedgerBalanceBillwiseSerializer(ledger_balance_billwise_instance, data=context)
                            if not serializer.is_valid():
                                return Response({
                                    'success': False,
                                    'message': get_error(serializer.errors),
                                    })
                            serializer.save()

                        else:
                            return Response({
                            'success': False,
                            'message': 'You are not allowed to Add ledger balance billwise',
                        })
                    else:
                        if user_permission_cr:
                            temp =i
                            temp.update({"fc_name":fc_name})
                            temp.update({"ledger_bal_id": ledger_bal_instance.id})
                            temp.update({"company_master_id":request.data['company_master_id']})
                            if D(i['fc_amount']) == 0:
                                fc_rate = "0"
                            else:
                                fc_rate = str(D(i['amount'])/D(i['fc_amount']))
                            if fc_rate[0] == "-":
                                fc_rate = fc_rate[1:]
                            fc_rate = round(D(fc_rate), 4)
                            temp.update({"fc_rate": fc_rate})
                        
                            temp['amount'] = D(temp['amount'])
                            temp['fc_amount'] = D(temp['fc_amount'])

                            if i['cr'] == 0:
                                temp['cr'] = 0
                    
                            if i['dr'] == 0:
                                temp['dr'] = 0
                                temp['amount'] = -temp['amount']
                                temp['fc_amount'] = -temp['fc_amount']

                            serializer = LedgerBalanceBillwiseSerializer(data=temp)
                            if not serializer.is_valid():
                                return Response({
                                    'success': False,
                                    'message': get_error(serializer.errors),
                                    })
                            serializer.save()
                        else:
                            return Response({
                            'success': False,
                            'message': 'You are not allowed to Add ledger balance billwise',
                        })

                update_ledger_balance(ledger_bal_instance.id)
                return Response({
                            'success': True,
                            'message': 'Ledger Balance Billwise Edited/Added Successfully',
                        })
            except:
                pass 
            user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
            if user_permission:  

                dr = 0
                cr = 0
                balance = 0
                fc_amt = 0
                # print(request.data['billwise'])
                for i in request.data['billwise']:
                    if i['dr']:
                        dr += D(i['dr'])
                        balance += D(i['dr'])
                        curr_add = D(i['dr'])
                        fc_amt += D(i['fc_amount'])

                    if i['cr']:
                        cr += i['cr']
                        balance -= D(i['cr']) 
                        curr_add = D(i['cr'])
                        fc_amt -= D(i['fc_amount'])
                    
                if fc_amt == 0:
                    fc_rate = "0"
                else:
                    fc_rate = str(balance/fc_amt)
                if request.data['fc_name']:
                    fc_name = request.data['fc_name']
                else:
                    fc_name = company_master.objects.get(id=request.data['company_master_id']).base_currency.id
                
                if balance < 0:
                    dr = 0
                    str_bal = str(balance)
                    str_bal = str_bal[1:]
                    cr = str_bal
                else:
                    cr = 0
                    dr = balance

                if fc_rate[0] == "-":
                    fc_rate = fc_rate[1:]
                fc_rate = round(D(fc_rate), 4)
                ledger_bal = ledger_balance(ledger_id_id=ledger_id, year_id_id=year_id, dr=dr, cr=cr,total_dr=dr, total_cr=cr, balance=balance, fc_amount= fc_amt, fc_name_id=fc_name, fc_rate=fc_rate, created_by=user.email, company_master_id_id=request.data['company_master_id'])
                ledger_bal.save()
                
                ledger_bal_id = ledger_balance.objects.latest('id').id
                ledger_bal_instance = ledger_balance.objects.latest('id')
                
                for i in request.data['billwise']:
                    temp =i
                    temp.update({"fc_name":fc_name})
                    temp.update({"ledger_bal_id": ledger_bal_id})
                    temp.update({"company_master_id":request.data['company_master_id']})
                    if D(i['fc_amount']) == 0:
                        fc_rate = "0"
                    else:
                        fc_rate = str(D(i['amount'])/D(i['fc_amount']))
                    if fc_rate[0] == "-":
                        fc_rate = fc_rate[1:]
                    fc_rate = round(D(fc_rate), 4)
                    temp.update({"fc_rate": fc_rate})
                

                    if temp['cr'] is None:
                        temp['cr'] = 0
                    

                    if temp['dr'] is None:
                        temp['dr'] = 0
                    # else:
                    #      i['amount'] = (-1)*D(i['amount'])
                    #      i['fc_amount'] = (-1)*D(i['fc_amount'])

                    serializer = LedgerBalanceBillwiseSerializer(data=temp)
                    if not serializer.is_valid():
                        ledger_bal_instance.dr = 0
                        ledger_bal_instance.cr = 0
                        ledger_bal_instance.total_dr = 0
                        ledger_bal_instance.total_cr = 0
                        ledger_bal_instance.balance = 0
                        ledger_bal_instance.fc_amount = 0
                        ledger_bal_instance.fc_rate = 0
                        ledger_bal_instance.save()
                        return Response({
                            'success': False,
                            'message': get_error(serializer.errors),
                            })
                dr_led = 0
                balance_led = 0
                curr_add_led = 0
                fc_amt_led = 0
                cr_led = 0
                
                for i in request.data['billwise']:
                    
                    temp1 =i
                    temp1.update({"fc_name":fc_name})
                    temp1.update({"ledger_bal_id": ledger_bal_id})
                    temp1.update({"company_master_id":request.data['company_master_id']})
                    if D(i['fc_amount']) == 0:
                        fc_rate = "0"
                    else:
                        fc_rate = str(D(i['amount'])/D(i['fc_amount']))
                    if fc_rate[0] == "-":
                        fc_rate = fc_rate[1:]
                    fc_rate = round(D(fc_rate), 4)
                    temp1.update({"fc_rate": fc_rate})
                    temp1['amount'] = D(i['amount'])
                    temp1['fc_amount'] = D(i['fc_amount'])
                    
                    if i['cr'] == 0:
                        temp1['cr'] = 0
            
                    if i['dr'] == 0:
                        temp1['dr'] = 0
                        print("hello", temp1['amount'])
                        temp1['amount'] = -temp1['amount']
                        temp1['fc_amount'] = -temp1['fc_amount']
                
                        
                    

                    print(temp1['amount'], temp1['fc_amount'])  
                    
                    #ledger balance
                
                    if D(i['dr']) != None:
                        dr_led += D(i['dr'])
                        balance_led += D(i['dr'])
                        curr_add_led = D(i['dr'])
                        fc_amt_led += D(i['fc_amount'])

                    if D(i['cr']) != None:
                        cr_led += i['cr']
                        balance_led -= D(i['cr']) 
                        curr_add_led = D(i['cr'])
                        fc_amt_led -= D(i['fc_amount'])
                    
                    #ledger balance finished


                    serializer = LedgerBalanceBillwiseSerializer(data=temp1)
                    if not serializer.is_valid():
                        
                        return Response({
                            'success': False,
                            'message':get_error(serializer.errors),
                            })
                    serializer.save()
                update_ledger_balance(ledger_bal_id)
                
                return Response({
                    'success': True,
                    'message': 'ledger balance billwise added successfully'
                    })
            else:
                return Response({
                    'success': False,
                    'message': 'You are not allowed to Add ledger balance billwise',
                })
                


# API For adding existing Ledger balance billwise together
# request : POST
# endpoint : add-all-ledger-bal-billwise
class AddExistingLedgerBalBillwise(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        user_permission = check_user_company_right("Opening Balance", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            ledger_bal_id = request.data['ledger_bal_id']
            fc_name = request.data['fc_name']
            
            for i in request.data['billwise']:
                temp =i
                temp.update({"fc_name":fc_name})
                temp.update({"ledger_bal_id": ledger_bal_id})
                temp.update({"company_master_id":request.data['company_master_id']})
                if D(i['fc_amount']) == 0:
                    fc_rate = "0"
                else:
                    fc_rate = str(D(i['amount'])/D(i['fc_amount']))
                if fc_rate[0] == "-":
                    fc_rate = fc_rate[1:]
                fc_rate = round(D(fc_rate), 4)
                temp.update({"fc_rate": fc_rate})

                if temp['cr'] is None:
                    temp['cr'] = 0
               
                
                if temp['dr'] is None:
                    temp['dr'] = 0
                
                serializer = LedgerBalanceBillwiseSerializer(data=temp)
                if not serializer.is_valid():
                    return Response({
                        'success': False,
                        'message': serializer.errors,
                        })
            total_bal_led = 0
            fc_amt_led = 0
            led_dr = 0
            led_cr = 0
            for i in request.data['billwise']:
                temp =i
                temp.update({"fc_name":fc_name})
                temp.update({"ledger_bal_id": ledger_bal_id})
                temp.update({"company_master_id":request.data['company_master_id']})
                if D(i['fc_amount']) == 0:
                    fc_rate = "0"
                else:
                    fc_rate = str(D(i['amount'])/D(i['fc_amount']))
                if fc_rate[0] == "-":
                    fc_rate = fc_rate[1:]
                fc_rate = round(D(fc_rate), 4)
                temp.update({"fc_rate": fc_rate})
                
                if temp['cr'] == 0:
                    temp['cr'] = 0
                    temp['fc_amount'] = D(i['fc_amount'])
                    temp['amount'] = D(i['amount'])
                    total_bal_led += D(temp['amount'])
                    fc_amt_led += D(temp['fc_amount'])
                if temp['dr'] == 0:
                    temp['dr'] = 0
                    temp['fc_amount'] = (-1)*D(i['fc_amount'])
                    temp['amount'] = (-1)*D(i['amount'])
                    total_bal_led -= D(temp['amount'])
                    fc_amt_led -= D(temp['fc_amount'])
                            
                
                
                serializer = LedgerBalanceBillwiseSerializer(data=temp)
                if not serializer.is_valid():
                    return Response({
                        'success': False,
                        'message': serializer.errors,
                        })
                serializer.save()
            update_ledger_balance(request.data['ledger_bal_id'])
            
            return Response({
                'success': True,
                'message': 'ledger balance billwise added successfully'
                })
        else:
            return Response({
            'success': False,
            'message': 'You are not allowed to Add ledger balance billwise',
            })
            
                
