from django.shortcuts import render
from rest_framework import response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from Company.models import user_company
from Company.models import user_group
import jwt, datetime
from django.http import JsonResponse
from django.http.response import HttpResponse
from .serializers import *


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
        check_transaction_right = transaction_right.objects.filter(transactions=transaction_rights)[0].id
        check_user_group = user_company.objects.get(user=user_id, company_master_id=user_company_id).user_group_id.id
        transaction_right_instance = transaction_right.objects.get(id=check_transaction_right)
        user_group_instance = user_group.objects.get(id=check_user_group)
        check_user_right = user_right.objects.get(user_group_id=user_group_instance, transaction_id=transaction_right_instance)
    except:
        return False
    if need_right=="can_create":
        return check_user_right.can_create
    elif need_right=="can_alter":
        return check_user_right.can_alter
    elif need_right=="can_delete":
        return check_user_right.can_delete
    else:
        return check_user_right.can_view

    

# API For getting user company in which user is included
# request : GET
class GetUserCompanyView(APIView):
    def get(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        user_company_query = user_company.objects.filter(user=user.id)
        companies=[]
        for i in user_company_query:
            if str(i.company_master_id.logo) == "":
                logo_str = None
            else:
                logo_str = str("/media/"+str(i.company_master_id.logo))
            
            companies.append({"company_id":i.company_master_id.id,"company_name":i.company_master_id.company_name, "logo": logo_str, "created_on": i.company_master_id.created_on})
        # print(companies)
        return Response({
                "success":True,
                "message":"",
                "data":
                {
                    "user_id":user.id,
                    "companies":companies
                }
        })


# Reusable function to insert data into year master
def year_master_insert(start_date, end_date, company_id, user_email):
    new_year_master= year_master(start_date=start_date, end_date=end_date, company_master_id=company_id, created_by=user_email)
    new_year_master.save()

# Reusable function to insert data into year voucher type
def voucher_type_insert(voucher_name, voucher_class, company_id, user_email):
    for i in range(len(voucher_name)):
        new_voucher_type = voucher_type(voucher_name=voucher_name[i], voucher_class=voucher_class[i], company_master_id = company_id, created_by = user_email)
        new_voucher_type.save()

# Reusable function to insert data into year account head
def acc_head_insert(acc_head_fields, company_id, user_email):
    for i in acc_head_fields:
        new_acc_head = acc_head(acc_head_name=i[0], title=i[1], company_master_id=company_id, bs=i[2],schedule_no=i[3],created_by=user_email )
        new_acc_head.save()

# Reusable function to insert data into year account group
def acc_group_insert(acc_group_fields, company_id, user_email):
    for i in acc_group_fields:
        try:
            new_acc_group = acc_group(group_name=i[0], acc_head_id = i[1], child_of=i[2], group_code=i[3], company_master_id=company_id, created_by=user_email)
            new_acc_group.save()
        except:
            new_acc_group = acc_group(group_name=i[0], acc_head_id = i[1], group_code=i[2], company_master_id=company_id, created_by=user_email)
            new_acc_group.save()


# Reusable function to insert data into year legder master
def ledger_master_insert(ledger_master_fields, company_id, user_email):
    for i in ledger_master_fields:
        new_ledger_master = ledger_master(ledger_id=i[0], ledger_name=i[1], acc_group_id=i[2], maintain_billwise=i[3], company_master_id=company_id, created_by=user_email)
        new_ledger_master.save()
          
# Reusable function to insert data into user_company
def user_company_insert(user, user_group_id, company_master_id, user_email):
    new_user_company= user_company(user=user, user_group_id=user_group_id, company_master_id=company_master_id, created_by=user_email)
    new_user_company.save()

# API For creating company
# request : POST
class CreateCompanyView(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_create_company:
            serializer = CompanySerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": {
                    "email":user.email
                }
                })

            serializer.save()
            added_company = company_master.objects.latest('id')
            company_user_group = user_group.objects.get(id=1)
            #Trigger data to user_company table
            user_company_insert(user,company_user_group,added_company,user.email)

            # Trigger data to year master
            year_master_insert(added_company.year_start_date, added_company.year_end_date, added_company, user.email)

            # Trigger data to voucher type
            voucher_name = ["Cash Sales", "Credit Sales", "Cash Purchase" ,"Credit Purchase" ,"Journal" ,"Contra" ,"Cash Receipt" ,"Bank Receipt" ,"Cash Payment" ,"Bank Payment" ,"memo" ,"planning" ,"debit note" ,"credit note"]
            voucher_class = ["Cash Sales", "Credit Sales", "Cash Purchase" ,"Credit Purchase" ,"Journal" ,"Contra" ,"Cash Receipt" ,"Bank Receipt" ,"Cash Payment" ,"Bank Payment" ,"memo" ,"planning" ,"debit note" ,"credit note"]
            voucher_type_insert(voucher_name, voucher_class, added_company, user.email)

            # Trigger data to account head
            
            account_head = [["Non - Current Assets", "ASSETS", True, 1], ["Current Assets", "ASSETS", True, 2], ["Equity", "EQUITY AND LIABILITIES", False, 3], ["Non-Current Liabilities",	"EQUITY AND LIABILITIES", False, 4], ["Current Liabilities", "EQUITY AND LIABILITIES",	False,	5],
             ["Income", "income",False,	6], ["Cost of Sales", "expenses", False, 7], ["Expenses", "expenses", False, 8]]
            acc_head_insert(account_head, added_company, user.email)
            
            # Trigger data to account group 

            non_current_assests = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Non - Current Assets")
            current_assests = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Current Assets")
            equity = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Equity")
            non_current_liabilities = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Non-Current Liabilities")
            current_liabilities = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Current Liabilities")
            income = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Income")
            cost_of_sales = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Cost of Sales")
            expenses = acc_head.objects.get(company_master_id=added_company.id, acc_head_name="Expenses")
            
            account_group = [ ["Property, Plant & Equipment", non_current_assests, "PPE"], ["Inventory", current_assests, "INV"],["Trade and other receivables", current_assests, "TOR"],["Cash and bank equivalents",	current_assests, "CB"], 
            ["Capital", equity,"CAP"],["Retained Earnings",	equity, "RE"],["Borrowings", non_current_liabilities, "BO"],["Employees end of service benefit",non_current_liabilities,	"ESB"],["Trade Payables and Others", current_liabilities, "TOP"],
            ["Borrowings-ShortTerm", current_liabilities, "BOS"],["Cash in Hand", current_assests, "Cash and bank equivalents",	"CAS"],["Cash at Bank",	current_assests, "Cash and bank equivalents", "BNK"],["Receivables",	current_assests, "Trade and other receivables",	"DR"],
            ["Payables", current_liabilities, "Trade Payables and Others", "CR"],["Revenue",	income, "REV"],["cost of sales",expenses, "COS"],["Other gains and losses", expenses,	"OGI"],["Administrative & Selling Expenses", expenses, "AOS"],["Finance costs", expenses, "FC"],
            ["Opening Stock", cost_of_sales, "OS",],["Closing Stock", cost_of_sales, "CS"],["Bank OD", current_liabilities, "BOD"]]
            acc_group_insert(account_group, added_company, user.email)

            # Trigger data to ledger master
            cash_in_hand = acc_group.objects.get(company_master_id=added_company.id, group_name="Cash in Hand")
            reatained_earnings = acc_group.objects.get(company_master_id=added_company.id, group_name="Retained Earnings")


            ledger_master = [["CAS-1", "cash", cash_in_hand, False], ["P&L", "Profit & Loss A/c" , reatained_earnings, False]]
            ledger_master_insert(ledger_master, added_company, user.email)
            
            #trigger all tables data
            return Response({
                "success":True,
                "message":"Company created successfully",
                "data":serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to Create Company",
            "data": {
                    "email":user.email
                }
            })



# API For editing company
# request : PUT
class EditCompanyView(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_edit_company:
            company_instance = company_master.objects.get(id=id)
            serializer = CompanySerializer(company_instance, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
            return Response({
                'success': True,
                'message': 'Company Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit Company',
                })
        

# API for deleting company
# request : DELETE        
class DeleteCompanyView(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_delete_company:
            company_master_record = company_master.objects.get(id=id)
            company_master_record.delete()
            return Response({
                'success': True,
                'message': 'Company deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Delete Company',
                })


# API For getting all details of all companies of a user
# request : GET
class DetailCompanyView(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_view_company:
            company_master_record = company_master.objects.get(id=id)
            serializer = GetCompanySerializer(company_master_record)
            return Response({
            'success': True,
            'message':'',
            'data':serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to View Company Details',
            })


# API For adding company document
# request : POST
class AddCompanyDocument(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_create_company:
            serializer = CompanyDocumentSerializer(data = request.data)
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
                "message":"Company Document added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                "success":False,
                "message":"Not authorized to Add Company Documents",
                "data":{
                    "email":user.email
                }
            })



# API For editing company document
# request : PUT
class EditCompanyDocumentView(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_edit_company:
            company_document_instance = company_master_docs.objects.get(id=id)
            serializer = CompanyDocumentSerializer(company_document_instance, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
            return Response({
                'success': True,
                'message': 'Company Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit Company Document',
                })



# API For deleting company document
# request : DELETE
class DeleteCompanyDocument(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_delete_company:
            company_master_documents = company_master_docs.objects.get(id=id)
            company_master_documents.delete()
            return Response({
                'success': True,
                'message': 'Company Document deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Delete Company Document',
                })
    

# API For getting company document
# request : GET
class GetCompanyDocumentView(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_view_company:
            company_master_record = company_master_docs.objects.filter(company_master_id=id)
            serializer = GetCompanyDocumentSerializer(company_master_record, many=True)
            return Response({
            'success': True,
            'message':'',
            'data':serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to View Company Document',
            })


# API For adding Currency
# request : POST
class AddCurrency(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_create_company:
            serializer = CurrencySerializer(data = request.data)
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
                "message":"Currency added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                "success":False,
                "message":"Not authorized to Add currency",
                "data":{
                    "email":user.email
                }
            })


# API For editing currency
# request : PUT
class EditCurrency(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_edit_company:
            currency_instance = currency.objects.get(id=id)
            serializer = CurrencySerializer(currency_instance, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
            return Response({
                'success': True,
                'message': 'Currency Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit Currency',
                })


# API For deleting currency
# request : DELETE
class DeleteCurrency(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_delete_company:
            company_master_documents = currency.objects.get(id=id)
            company_master_documents.delete()
            return Response({
                'success': True,
                'message': 'Currency deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Currency',
                })


# API For getting currency
# request : GET
class GetCurrency(APIView):
    def get(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_view_company:
            all_currency = currency.objects.all()
            serializer = CurrencySerializer(all_currency, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to View Company Document',
            })


# API For adding voucher type
# request : POST
class AddVoucherType(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        serializer = VoucherTypeSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
            "success":False,
            "message": get_error(serializer.errors),
            })

        serializer.save()
        return Response({
            "success":True,
            "message":"Voucher Type added successfully",
            "data":serializer.data
            })




# API For editing Voucher Type
# request : PUT
class EditVoucherType(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        voucher_type_instance = voucher_type.objects.get(id=id)
        print(voucher_type_instance)
        serializer = VoucherTypeSerializer(voucher_type_instance, data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': get_error(serializer.errors),
                })
                
        serializer.save()
        return Response({
            'success': True,
            'message': 'Voucher Type Edited successfully'})
        

# API For deleting vouhcer
# request : DELETE
class DeleteVoucherType(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        voucher_type_record = voucher_type.objects.get(id=id)
        voucher_type_record.delete()
        return Response({
            'success': True,
            'message': 'Voucher deleted Successfully',
            })


# API For getting voucher type
# request : GET
class GetVoucherType(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # id is company id
        voucher_type_record = voucher_type.objects.filter(company_master_id=id)
        serializer = GetVoucherTypeSerializer(voucher_type_record, many=True)
        return Response({
        'success': True,
        'message':'',
        'data': serializer.data
        })


# API For adding Account Head
# request : POST
class AddAccountHead(APIView):
    def post(self, request):
        payload = verify_token(request)

        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        user_permission = check_user_company_right("Account Head", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            print(request.data)
            last_comp_schedule_no = acc_head.objects.filter(company_master_id=request.data['company_master_id'])
            new_schedule_no = len(last_comp_schedule_no)+1
            request.data.update({"schedule_no":new_schedule_no})
            serializer = AccountHeadSerializer(data = request.data)
            print(request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message": get_error(serializer.errors),
                })

            serializer.save()
            return Response({
                "success":True,
                "message":"Account Head added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Add Account Head',
            })


# API For editing Account Head
# request : PUT
class EditAccountHead(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        acc_head_instance = acc_head.objects.get(id=id)
        if acc_head_instance.is_fixed:
             return Response({
                'success': False,
                'message': 'You are not allowed to Edit Account Head',
            })
        user_permission = check_user_company_right("Account Head", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            request.data.update({"schedule_no":acc_head_instance.schedule_no})
            serializer = AccountHeadSerializer(acc_head_instance, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
            return Response({
                'success': True,
                'message': 'Account Head Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Add Account Head',
            })
        


# API For deleting vouhcer
# request : DELETE
class DeleteAccountHead(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        acc_head_instance = acc_head.objects.get(id=id)
        if acc_head_instance.is_fixed:
             return Response({
                'success': False,
                'message': 'You are not allowed to Delete Account Head',
            })
        user_permission = check_user_company_right("Account Head", acc_head_instance.company_master_id, user.id, "can_delete")
        if user_permission:
            acc_head_instance.delete()
            return Response({
                'success': True,
                'message': 'Account Head deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to delete Account Head',
            })



# API For getting voucher type
# request : GET
class GetAccountHead(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # id is company id
        user_permission = check_user_company_right("Account Head", id, user.id, "can_view")
        if user_permission:
            acc_head_instance = acc_head.objects.filter(company_master_id=id)
            serializer = AccountHeadSerializer(acc_head_instance, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Account Head',
            })


#aayush api don't touch
# API For adding Cost Category
# request : POST
class AddCostCategory(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        user_permission = check_user_company_right("Cost Category", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            serializer = CostCategorySerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message": get_error(serializer.errors),
                })

            serializer.save()
            return Response({
                "success":True,
                "message":"Cost Category added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                "success":False,
                "message":"You are not allowed to add Cost Category"
                })            



#aayush api don't touch
# API For editing Cost Category
# request : PUT
class EditCostCategory(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        user_permission = check_user_company_right("Cost Category", request.data['company_master_id'], user.id, "can_edit")
        if user_permission:
            cost_category_instance = cost_category.objects.get(id=id)
            # print(cost_category_instance)
            serializer = CostCategorySerializer(cost_category_instance, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
            return Response({
                'success': True,
                'message': 'Cost Category Edited successfully'})
        else:
            return Response({
                "success":False,
                "message":"You are not allowed to Edit Cost Category"
                })        

#aayush api don't touch
# API For deleting Cost Category
# request : DELETE
class DeleteCostCategory(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        cost_category_instance = cost_category.objects.get(id=id)
        user_permission = check_user_company_right("Cost Category", cost_category_instance.company_master_id, user.id, "can_delete")
        if user_permission:
            cost_category_instance = cost_category.objects.get(id=id)
            cost_category_instance.delete()
            return Response({
                'success': True,
                'message': 'Cost Category deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Delete Cost Category',
                })

#aayush api don't touch 
# API For getting Cost Category
# request : GET
class GetCostCategory(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
       
        user_permission = check_user_company_right("Cost Category", id , user.id, "can_view")
        if user_permission:
            cost_category_instance = cost_category.objects.filter(company_master_id=id)
            serializer = CostCategorySerializer(cost_category_instance, many=True)
            return Response({
            'success': True,
            'message':'',
            'data':  serializer.data
            
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to View Cost Categories',
            })            


#jevin api don't touch 
# API For adding acc_group type
# request : POST
class AddAccGroup(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        serializer = AccGroupSerializer(data = request.data)
        user_permission = check_user_company_right("Account Group", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message": get_error(serializer.errors),
                })

            serializer.save()
            return Response({
                "success":True,
                "message":"account group added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to add Account group',
                }) 

# API For editing Voucher Type
# request : PUT
class EditAccGroup(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        accgroup_instance = acc_group.objects.get(id=id)
        if(accgroup_instance.is_fixed):
            return Response({
            'success': False,
            'message': 'You cannot edit Account group',
            })
        user_permission = check_user_company_right("Account Group", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            serializer = AccGroupSerializer(accgroup_instance, data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
            return Response({
                'success': True,
                'message': 'Account Group Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit Account group',
                }) 

        

# API For deleting account group
# request : DELETE
class DeleteAccGroup(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        acc_group_record = acc_group.objects.get(id=id)
        if(acc_group_record.is_fixed):
            return Response({
            'success': False,
            'message': 'You cannot delete this field',
            })
        user_permission = check_user_company_right("Account Group", acc_group_record.company_master_id, user.id, "can_delete")
        if user_permission:
            acc_group_record.delete()
            return Response({
                'success': True,
                'message': 'Account group deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to delete this field',
                }) 


# API For getting account group
# request : GET
class GetAccGroup(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # id is company id
        user_permission = check_user_company_right("Account Group", id, user.id, "can_view")
        if user_permission:
            acc_group_record = acc_group.objects.filter(company_master_id=id)
            serializer = AccGroupSerializer(acc_group_record, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view Account group',
                }) 

# jevin api finished