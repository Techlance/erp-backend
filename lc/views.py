from rest_framework.views import APIView
from rest_framework.response import Response
from .models import lc, lc_docs, lc_amend
from Company.models import user_company
from Company.models import user_group
import jwt
from django.http import JsonResponse
from django.http.response import HttpResponse
from .serializers import LCAmendSerializer, GetLCDocsSerializer, LCDocsSerializer, LCSerializer, GetLCSerializer
from Company.models import company_master, company_master_docs
from Users.models import User, transaction_right, user_right



# Create your views here.

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



############################################################################################################################
##################################################  LC(CRUD) ###############################################################
############################################################################################################################


# API For Adding LC
# request : POST
# endpoint : add-lc/<int:id>
class AddLC(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        # permission
        user_permission = check_user_company_right("LC", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            temp = request.data
            context = temp.dict()
            context['altered_by'] = user.email
            serializer = LCSerializer(data = context)
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
                "message":"LC added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                "success":False,
                "message":"Not authorized to Add LC",
                "data":{
                    "email":user.email
                }
            })


# API For editing LC
# request : PUT
# endpoint : edit-lc/<int:id>
class EditLC(APIView):
    def put(self, request, id):
        # verfiy token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission : to edit LC
        user_permission = check_user_company_right("LC", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            lc_instance = lc.objects.get(lc_no=id)
            temp = request.data
            context = temp.dict()
            context['altered_by'] = user.email
            serializer = LCSerializer(lc_instance, data=context)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'LC edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit LC',
                })


# API For deleting LC
# request : DELETE
# endpoint : delete-lc/<int:id>
class DeleteLC(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission : inherited from can edit company
        lc_instance = lc.objects.get(lc_no=id)
        user_permission = check_user_company_right("LC", lc_instance.company_master_id, user.id, "can_delete")
        if user_permission:
            lc_instance.altered_by = user.email
            lc_instance.delete()
            return Response({
                'success': True,
                'message': 'LC deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to delete LC',
                })


# API For getting LC data
# request : GET
# endpoint : get-lc
class GetLC(APIView):
    def get(self, request, id):
        # verify token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        user_permission = check_user_company_right("LC", id, user.id, "can_view")
        if user_permission:
            all_lc = lc.objects.filter(company_master_id=id)
            serializer = GetLCSerializer(all_lc, many=True)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view LC',
                })


# API For getting LC data
# request : GET
# endpoint : get-detail-lc
class GetDetailLC(APIView):
    def get(self, request, id):
        # verify token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        lc_instance = lc.objects.get(lc_no=id)
        user_permission = check_user_company_right("LC", lc_instance.company_master_id, user.id, "can_view")
        if user_permission:
           
            serializer = GetLCSerializer(lc_instance)
            return Response({
            'success': True,
            'message':'',
            'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view LC',
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
        
        user_permission = check_user_company_right("LC", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            temp = request.data
            context = temp.dict()
            context['altered_by'] = user.email
            serializer = LCDocsSerializer(data = context)
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
        else:
            return Response({
                "success":False,
                "message":"Not authorized to Add LC Document",
                "data":{
                    "email":user.email
                }
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

        user_permission = check_user_company_right("LC", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            lc_document_instance = lc_docs.objects.get(id=id)
            temp = request.data
            context = temp.dict()
            context['altered_by'] = user.email
            serializer = LCDocsSerializer(lc_document_instance, data=context)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
              
            serializer.save()
            
            return Response({
                'success': True,
                'message': 'LC Document Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit LC Document',
                })
            


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
        lc_instance = lc.objects.get(lc_no=lc_document.lc_id.lc_no)
        user_permission = check_user_company_right("LC", lc_instance.company_master_id, user.id, "can_delete")
        if user_permission:
            lc_document.altered_by = user.email
            lc_document.delete()
            return Response({
                'success': True,
                'message': 'LC Document deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to delete LC Document',
                })




# API For getting lc document
# request : GET
# endpoint : get-lc-document/<int:id>
class GetLcDocuments(APIView):
    def get(self, request, id):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()  
        except:
            return payload 
        
        # Fetches lc_docs record corresponding to the document_id
        lc_instance = lc.objects.get(lc_no=id) 
        user_permission = check_user_company_right("LC", lc_instance.company_master_id, user.id, "can_view")
        if user_permission:
            lc_docs_record = lc_docs.objects.filter(lc_id=id)
            serializer = GetLCDocsSerializer(lc_docs_record, many=True)
            return Response({
            'success': True,
            'message':'',
            'data':serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view LC Document',
                })


#API for downloading lc document
# request : GET
# endpoint : download-lc-document/<int:id>
class DownloadLcDoc(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()  
        except:
            return payload 
        lc_doc = lc_docs.objects.get(id=id) 
        user_permission = check_user_company_right("LC", lc_doc.company_master_id, user.id, "can_view")
        if user_permission:
            
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
################################################## LC AMEND (CRUD) #########################################################
############################################################################################################################


# API For Adding LC
# request : POST
# endpoint : add-lc-amend
class AddLCAmend(APIView):
    def post(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission
        user_permission = check_user_company_right("LC", request.data['company_master_id'], user.id, "can_create")
        if user_permission:
            lc_count = int(lc_amend.objects.filter(lc_id=request.data['lc_id']).count()) + 1
            print(lc_count)
            temp = request.data
            context = temp.dict()
            context['altered_by'] = user.email
            context['amendment_no'] = lc_count
            serializer = LCAmendSerializer(data = context)
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
                "message":"Lc-Amend added successfully",
                "data":serializer.data
                })
        else:
            return Response({
                "success":False,
                "message":"Not authorized to Add LC-Amend",
                "data":{
                    "email":user.email
                }
            })


# API For editing lc amend
# request : PUT
# endpoint : edit-lc-amend/<int:id>
class EditLCAmend(APIView):
    def put(self, request, id):
        # verfiy token
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        # permission : inherited from can edit company
        user_permission = check_user_company_right("LC", request.data['company_master_id'], user.id, "can_alter")
        if user_permission:
            lc_amend_instance = lc_amend.objects.get(id=id)
            temp = request.data
            context = temp.dict()
            context['altered_by'] = user.email
            serializer = LCAmendSerializer(lc_amend_instance, data=context)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })

            serializer.save()
            return Response({
                'success': True,
                'message': 'LCAmend edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to LC Amend',
                })


# API For deleting LC Amend
# request : DELETE
# endpoint : delete-lc-amend/<int:id>
class DeleteLCAmend(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        lc_amend_instance = lc_amend.objects.get(id=id)
        user_permission = check_user_company_right("LC", lc_amend_instance.company_master_id, user.id, "can_delete")
        if user_permission:
        
            lc_amend_instance.altered_by = user.email
            lc_amend_instance.delete()
            return Response({
                'success': True,
                'message': 'LCAmend deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to deleteLC Amend',
                })


# API For getting LC-amend data
# request : GET
# endpoint : get-lc-amend/<int:id>
class GetLCAmend(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        lc_amend_instance = lc_amend.objects.filter(lc_id=id)
        lc_instance = lc.objects.get(lc_no=id)
        user_permission = check_user_company_right("LC", lc_instance.company_master_id, user.id, "can_view")
        if user_permission:
            
            serializer = LCAmendSerializer(lc_amend_instance, many=True)
            return Response({
                'success': True,
                'message': '',
                'data':serializer.data
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to view LC Amend',
                })
        