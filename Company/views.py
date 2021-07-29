from django.shortcuts import render
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
            companies.append({"company_id":i.company_master_id.id,"company_name":i.company_master_id.company_name})
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


def year_master_insert(start_date, end_date, company_id, user_email):
    new_year_master= year_master(start_date=start_date, end_date=end_date, company_master_id=company_id, created_by=user_email)
    new_year_master.save()

def voucher_type_insert(voucher_name, voucher_class, company_id, user_email):

    for i in range(len(voucher_name)):
        new_voucher_type = voucher_type(voucher_name=voucher_name[i], voucher_class=voucher_class[i], company_master_id = company_id, created_by = user_email)
        new_voucher_type.save()

def acc_head_insert(acc_head_fields, company_id, user_email):
    for i in acc_head_fields:
        new_acc_head = acc_head(acc_head_name=i[0], title=i[1], company_master_id=company_id, bs=i[2],schedule_no=i[3],created_by=user_email )
        new_acc_head.save()

def acc_group_insert(acc_group_fields, company_id, user_email):
    for i in acc_group_fields:
        try:
            new_acc_group = acc_group(group_name=i[0], acc_head_id = i[1], child_of=i[2], group_code=i[3], company_master_id=company_id, created_by=user_email)
            new_acc_group.save()
        except:
            new_acc_group = acc_group(group_name=i[0], acc_head_id = i[1], group_code=i[2], company_master_id=company_id, created_by=user_email)
            new_acc_group.save()

def ledger_master_insert(ledger_master_fields, company_id, user_email):
    for i in ledger_master_fields:
        new_ledger_master = ledger_master()
          


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
            year_master_insert(added_company.start_date, added_company.end_date, added_company.id, user.email)

            # Trigger data to voucher type
            voucher_name = ["Cash Sales", "Credit Sales", "Cash Purchase" ,"Credit Purchase" ,"Journal" ,"Contra" ,"Cash Receipt" ,"Bank Receipt" ,"Cash Payment" ,"Bank Payment" ,"memo" ,"planning" ,"debit note" ,"credit note"]
            voucher_class = ["Cash Sales", "Credit Sales", "Cash Purchase" ,"Credit Purchase" ,"Journal" ,"Contra" ,"Cash Receipt" ,"Bank Receipt" ,"Cash Payment" ,"Bank Payment" ,"memo" ,"planning" ,"debit note" ,"credit note"]
            voucher_type_insert(voucher_name, voucher_class, added_company.id, user.email)

            # Trigger data to account head
            
            account_head = [["Non - Current Assets", "ASSETS", True, 1], ["Current Assets", "ASSETS", True, 2], ["Equity", "EQUITY AND LIABILITIES", False, 3], ["Non-Current Liabilities",	"EQUITY AND LIABILITIES", False, 4], ["Current Liabilities", "EQUITY AND LIABILITIES",	False,	5],
             ["Income", "income",False,	6], ["Cost of Sales", "expenses", False, 7], ["Expenses", "expenses", False, 8]]
            acc_head_insert(account_head, added_company.id, user.email)
            
            # Trigger data to account group 

            account_group = [ ["Property, Plant & Equipment", "Non - Current Assets", "PPEx"], ["Inventory"	"Current Assets", "INV"],["Trade and other receivables", "Current Assets", "TOR"],["Cash and bank equivalents",	"Current Assets", "CB"], 
            ["Capital", "Equity","CAP"],["Retained Earnings",	"Equity", "RE"],["Borrowings",	"Non-Current Liabilities", "BO"],["Employees end of service benefit",	"Non-Current Liabilities",	"ESB"],["Trade Payables and Others"	"Current Liabilities",	"TOP"],
            ["Borrowings-ShortTerm",	"Current Liabilities", "BOS"],["Cash in Hand",	"Current Assets	Cash and bank equivalents",	"CAS"],["Cash at Bank",	"Current Assets",	"Cash and bank equivalents",	"BNK"],["Receivables",	"Current Assets",	"Trade and other receivables",	"DR"],
            ["Payables",	"Current Liabilities", "Trade Payables and Others",	"CR"],["Revenue",	"Income", 	"REV"],["cost of sales",	"Expenses",		"COS"],["Other gains and losses	Expenses",	"OGI"],["Administrative & Selling Expenses",	"Expenses",	 "AOS"],["Finance costs",	"Expenses",		 "FC"],
            ["Opening Stock",	"cost of sales",  "OS",],["Closing Stock",	"cost of sales",  "CS"],["Bank OD",	"Current Liabilities",  "BOD"]]
            acc_group_insert(account_group, added_company.id, user.email)

            # Trigger data to ledger master

            ledger_master = [["CAS-1", "cash", "Cash in Hand", False], ["P&L", "Profit & Loss A/c"	"Retained Earnings"	, False]]
            
            #trigger all tables data
            return Response({
                "success":True,
                "message":"company created successfully",
                "data":serializer.data
                })
        else:
            return Response({
            "success":False,
            "message":"Not Allowed to Create Company",
            "data":user.email
            })

