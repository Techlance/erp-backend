from django.shortcuts import render
from rest_framework import response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from Company.models import user_company
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
            companies.append({"company_id":i.company_master_id.id,"company_name":i.company_master_id.company_name, "logo": str(i.company_master_id.logo), "created_on": i.company_master_id.created_on})
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
                "data": user.email
                })

            serializer.save()
            added_company = company_master.objects.latest('id')

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
            "data":user.email
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
            'data': {
                'data': serializer.data
            }
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to View Company Details',
            })


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
                "message": serializer.errors,
                "data": user.email
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
            'data': {
                'data': serializer.data
            }
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to View Company Document',
            })


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
                "message": serializer.errors,
                "data": user.email
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
            'data': {
                'data': serializer.data
            }
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to View Company Document',
            })
    