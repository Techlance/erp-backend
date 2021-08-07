from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from Company.models import user_company
from Company.models import user_group
import jwt
from django.http import JsonResponse
from django.http.response import HttpResponse
from .serializers import *
from Company.models import *
from Users.models import *



# Create your views here.

############################################################################################################################
##################################################  LC(CRUD) ###############################################################
############################################################################################################################


## LC

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


class AddLC(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission
        serializer = LCSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
            "success":False,
            "message": get_error(serializer.errors),
            "data": {
                "email":user.email
            }
            })

        company_master_instance = company_master.objects.get(id=request.data['company_master_id'])
        new_lc_logs = lc_logs(trans_type=request.data['trans_type'], lc_date=request.data['lc_date'], year_id=request.data['year_id'], party_code=request.data['party_code'], cost_center=request.data['cost_center'], applicant_bank=request.data['applicant_bank'],
        benificiary_bank=request.data['benificiary_bank'], benificiary_bank_lc_no=request.data['benificiary_bank_lc_no'], applicant_bank_lc_no=request.data['applicant_bank_lc_no'], inspection=request.data['inspection'], bank_ref=request.data['bank_ref'], days_for_submit_to_bank=request.data['days_for_submit_to_bank'], payment_terms=request.data['payment_terms'],
        place_of_taking_incharge=request.data['place_of_taking_incharge'], final_destination_of_delivery=request.data['final_destination_of_delivery'], completed=request.data['completed'], shipment_terms=request.data['shipment_terms'], goods_description=request.data['goods_description'], other_lc_terms=request.data['other_lc_terms'], 
        bank_ac=request.data['bank_ac'], expiry_date=request.data['expiry_date'], lc_amount=request.data['lc_amount'], company_master_id=company_master_instance, entry="after", is_deleted=False, operation="create", altered_by=user.email,)
        new_lc_logs.save()
        serializer.save()
    
        return Response({
            "success":True,
            "message":"LC added successfully",
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

# API For editing currency
# request : PUT
# endpoint : edit-currency/<int:id>
class EditLC(APIView):
    def put(self, request, id):
        # verfiy token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission : inherited from can edit company
        lc_instance = lc.objects.get(id=id)
        serializer = lc(lc_instance, data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': get_error(serializer.errors),
                })

        company_master_instance = company_master.objects.get(id=request.data['company_master_id'])
        new_lc_logs = lc_logs(trans_type=lc_instance.trans_type, lc_date=lc_instance.lc_date, year_id=lc_instance.year_id, party_code=lc_instance.party_code, cost_center=lc_instance.cost_center, applicant_bank=lc_instance.applicant_bank,
        benificiary_bank=lc_instance.benificiary_bank, benificiary_bank_lc_no=lc_instance.benificiary_bank_lc_no, applicant_bank_lc_no=lc_instance.applicant_bank_lc_no, inspection=lc_instance.inspection, bank_ref=lc_instance.bank_ref, days_for_submit_to_bank=lc_instance.days_for_submit_to_bank, payment_terms=lc_instance.payment_terms,
        place_of_taking_incharge=lc_instance.place_of_taking_incharge, final_destination_of_delivery=lc_instance.final_destination_of_delivery, completed=lc_instance.completed, shipment_terms=lc_instance.shipment_terms, goods_description=lc_instance.goods_description, other_lc_terms=lc_instance.other_lc_terms, 
        bank_ac=lc_instance.bank_ac, expiry_date=lc_instance.expiry_date, lc_amount=lc_instance.lc_amount, company_master_id=lc_instance.company_master_id.company_name, entry="before", is_deleted=False, operation="edit", altered_by=user.email,)
        new_lc_logs.save()
        new_lc_logs = lc_logs(trans_type=request.data['trans_type'], lc_date=request.data['lc_date'], year_id=request.data['year_id'], party_code=request.data['party_code'], cost_center=request.data['cost_center'], applicant_bank=request.data['applicant_bank'],
        benificiary_bank=request.data['benificiary_bank'], benificiary_bank_lc_no=request.data['benificiary_bank_lc_no'], applicant_bank_lc_no=request.data['applicant_bank_lc_no'], inspection=request.data['inspection'], bank_ref=request.data['bank_ref'], days_for_submit_to_bank=request.data['days_for_submit_to_bank'], payment_terms=request.data['payment_terms'],
        place_of_taking_incharge=request.data['place_of_taking_incharge'], final_destination_of_delivery=request.data['final_destination_of_delivery'], completed=request.data['completed'], shipment_terms=request.data['shipment_terms'], goods_description=request.data['goods_description'], other_lc_terms=request.data['other_lc_terms'], 
        bank_ac=request.data['bank_ac'], expiry_date=request.data['expiry_date'], lc_amount=request.data['lc_amount'], company_master_id=company_master_instance.company_name, entry="after", is_deleted=False, operation="edit", altered_by=user.email,)
        new_lc_logs.save()
        serializer.save()
        return Response({
            'success': True,
            'message': 'LC edited successfully'})
        # else:
        #     return Response({
        #         'success': False,
        #         'message': 'You are not allowed to edit Currency',
        #         })


class DeleteLC(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission : inherited from can edit company
        lc_instance = lc.objects.get(id=id)
        new_lc_logs = lc_logs(trans_type=lc_instance.trans_type, lc_date=lc_instance.lc_date, year_id=lc_instance.year_id, party_code=lc_instance.party_code, cost_center=lc_instance.cost_center, applicant_bank=lc_instance.applicant_bank,
        benificiary_bank=lc_instance.benificiary_bank, benificiary_bank_lc_no=lc_instance.benificiary_bank_lc_no, applicant_bank_lc_no=lc_instance.applicant_bank_lc_no, inspection=lc_instance.inspection, bank_ref=lc_instance.bank_ref, days_for_submit_to_bank=lc_instance.days_for_submit_to_bank, payment_terms=lc_instance.payment_terms,
        place_of_taking_incharge=lc_instance.place_of_taking_incharge, final_destination_of_delivery=lc_instance.final_destination_of_delivery, completed=lc_instance.completed, shipment_terms=lc_instance.shipment_terms, goods_description=lc_instance.goods_description, other_lc_terms=lc_instance.other_lc_terms, 
        bank_ac=lc_instance.bank_ac, expiry_date=lc_instance.expiry_date, lc_amount=lc_instance.lc_amount, company_master_id=lc_instance.company_master_id.company_name, entry="before", is_deleted=Tru, operation="delete", altered_by=user.email,)
        new_lc_logs.save()
        lc_instance.delete()
        return Response({
            'success': True,
            'message': 'LC deleted Successfully',
            })


# API For getting currency
# request : GET
# endpoint : get-currency
class GetLC(APIView):
    def get(self, request):
        # verify token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        all_lc = lc.objects.all()
        serializer = LCSerializer(all_lc, many=True)
        return Response({
        'success': True,
        'message':'',
        'data': serializer.data
        })

############################################################################################################################
################################################## LC DOCUMENTS (CRUD) #################################################
############################################################################################################################


# API For adding LC document
# request : POST
# endpoint : add-lc-document
class AddLCDoc(APIView):
    def post(self, request):
        # Verify Token for authorization 
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        serializer = LCDocsSerializer(data = request.data)
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
            "message":"LC Document added successfully",
            "data":serializer.data
            })



# API For editing lc document
# request : PUT
# endpoint : edit-lc-docment/<int:id>
class EditLcDoc(APIView):
    
    def put(self, request, id):
        
        payload = verify_token(request)
        
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload


        lc_document_instance = lc_docs.objects.get(id=id)
        serializer = LCDocsSerializer(lc_document_instance, data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': get_error(serializer.errors),
                })
        
        instance_lc = lc.objects.get(id=request.data['lc_id'])
        new_lc_docs_logs = lc_docs_logs(doc_name=lc_document_instance.doc_name, file=lc_document_instance.file, lc_id=lc_document_instance.lc_id.lc_no, entry="before", is_deleted=False, operation="edit", altered_by=user.email,)
        new_lc_docs_logs.save()
        
        
        serializer.save()
        lc_document_instance = lc_docs.objects.get(id=id)
        new_lc_docs_logs = lc_docs_logs(doc_name=lc_document_instance.doc_name, file=lc_document_instance.file, lc_id=lc_document_instance.lc_id.lc_no, entry="after", is_deleted=False, operation="edit", altered_by=user.email,)
        new_lc_docs_logs.save()
        
        return Response({
            'success': True,
            'message': 'LC Document Edited successfully'})
            


# API For deleting LC document
# request : DELETE
# endpoint : delete-lc-document/<int:id> 
class DeleteLcDoc(APIView):  
    def delete(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload



        lc_document = lc_docs.objects.get(id=id)
        lc_instance = lc.objects.get(id=lc_document.lc_id.id)
        new_lc_document_logs = lc_docs_logs(doc_name=lc_document.doc_name, file=lc_document.doc_name, lc_id=lc_instance.lc_no, entry="before", is_deleted=True, operation="delete", altered_by=user.email,)
        new_lc_document_logs.save()
        lc_document.delete()
        return Response({
            'success': True,
            'message': 'LC Document deleted Successfully',
            })


# API For getting lc document
# request : GET
# endpoint : get-lc-documents/<int:id>
class GetLcDocuments(APIView):
    def get(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()  
        except:
            return payload 
        
        # Fetches lc_docs record corresponding to the document_id 
        lc_docs_record = company_master_docs.objects.filter(lc_id=id)
        serializer = GetLCDocsSerializer(lc_docs_record, many=True)
        return Response({
        'success': True,
        'message':'',
        'data':serializer.data
        })




#API for downloading lc document
class DownloadLcDoc(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()  
        except:
            return payload 
        if user.is_superuser:
            lc_doc = lc_docs.objects.get(id=id)
            temp = lc_doc.file
            im = str(lc_doc.file)
            
            files = temp.read()
            ext = ""
            im = im[::-1]
            for i in im:
                if i==".":
                    break 
                else:
                    ext += i
            ext = ext[::-1]
            im = im[::-1]
            # print(im)
            file_name = im[6:]
            response = HttpResponse(files, content_type='application/'+ext)
            response['Content-Disposition'] = "attachment; filename="+file_name
            return response


############################################################################################################################
################################################## LC AMEND (CRUD) #################################################
############################################################################################################################


class AddLCAmend(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission
        serializer = LCAmendSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
            "success":False,
            "message": get_error(serializer.errors),
            "data": {
                "email":user.email
            }
            })


        lc_instance = lc.objects.get(id=request.data['lc_id'])
        new_lc_amend_logs = lc_amend_logs(lc_id=lc_instance.lc_no, amendment_no=request.data['amendment_no'], issue_date=request.data['issue_date'], LDS=request.data['LDS'], expiry_date=request.data['expiry_date'], lc_amount=request.data['lc_amount'],
        remarks=request.data['remarks'], entry="after", is_deleted=False, operation="create", altered_by=user.email)
        new_lc_amend_logs.save()
        serializer.save()
    
        return Response({
            "success":True,
            "message":"Lc-Amend added successfully",
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


# API For editing lcamend
# request : PUT
# endpoint : 
class EditLCAmend(APIView):
    def put(self, request, id):
        # verfiy token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission : inherited from can edit company
        lc_amend_instance = lc_amend.objects.get(id=id)
        serializer = LCAmendSerializer(lc_amend_instance, data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': get_error(serializer.errors),
                })

        lc_instance = lc.objects.get(id=request.data['lc_id'])
        new_lc_amend_logs = lc_amend_logs(lc_id=lc_amend_instance.lc_id, amendment_no=lc_amend_instance.amendment_no, issue_date=lc_amend_instance.issue_date, LDS=lc_amend_instance.LDS, expiry_date=lc_amend_instance.expiry_date, lc_amount=lc_amend_instance.lc_amount,
        remarks=lc_amend_instance.remarks, entry="before", is_deleted=False, operation="edit", altered_by=user.email)
        new_lc_amend_logs.save()
        new_lc_amend_logs = lc_amend_logs(lc_id=lc_instance.lc_no, amendment_no=request.data['amendment_no'], issue_date=request.data['issue_date'], LDS=request.data['LDS'], expiry_date=request.data['expiry_date'], lc_amount=request.data['lc_amount'],
        remarks=request.data['remarks'], entry="after", is_deleted=False, operation="create", altered_by=user.email)
        new_lc_amend_logs.save()
        serializer.save()
        return Response({
            'success': True,
            'message': 'LCAmend edited successfully'})
        # else:
        #     return Response({
        #         'success': False,
        #         'message': 'You are not allowed to edit Currency',
        #         })



class DeleteLCAmend(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        lc_amend_instance = lc_amend.objects.get(id=id)
        new_lc_amend_logs = lc_amend_logs(lc_id=lc_amend_instance.lc_id, amendment_no=lc_amend_instance.amendment_no, issue_date=lc_amend_instance.issue_date, LDS=lc_amend_instance.LDS, expiry_date=lc_amend_instance.expiry_date, lc_amount=lc_amend_instance.lc_amount,
        remarks=lc_amend_instance.remarks, entry="before", is_deleted=True, operation="delete", altered_by=user.email)
        new_lc_amend_logs.save()
        lc_amend_instance.delete()
        return Response({
            'success': True,
            'message': 'LCAmend deleted Successfully',
            })


class GetLCAmend(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        lc_amend_instance = lc_amend.objects.get(id=id)
        serializer = LCAmendSerializer(lc_amend_instance, many=True)
        return Response({
            'success': True,
            'message': '',
            'data':serializer.data
            })