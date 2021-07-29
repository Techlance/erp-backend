from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from Company.models import user_company
import jwt, datetime
from django.http import JsonResponse
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



# API For Login
# request : POST
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            context = {
                "success":False,
                "message":"User not found",
                "data":
                {
                    "email":email,
                }
            }
            return JsonResponse(context)

        if not user.check_password(password):
            context = {
                "success":False,
                "message":"In-correct password",
                "data":
                {
                    "email":email,
                }
            }
            return JsonResponse(context)

        payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=500),
                    'iat': datetime.datetime.utcnow()
                    }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8') #generating token
        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)
        response.data = {
                        "success":True,
                        "message":"User logged in successfully",
                        "data":
                            {
                            "accessToken":token,
                            "user":{
                                "id":user.id,
                                "email":user.email,
                                }
                            
                            }
                        }
        return response

# API to add user
# request : POST
# PENDING
class AddUserView(APIView):
    def post(self, request):
        # Verify token i.e checks user is authenticated or not
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        #checks user is superadmin or not
        # user_company_row = user_company.objects.filter(user=user.id).filter(company_master_id=company_id)
        # user_group_id = user_company_row.user_group_id
        # user_right_row = user_right.objects.filter(user_group_id=user_group_id).filter(transaction_id=9)
        # print(user_right_row.can_create)
        # if user_right_row.can_create:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                # "data": user.email
                })

            serializer.save()
            return Response({
                "success":True,
                "message":"User added successfully",
                "data":serializer.data
                })

        # else:
        #     return Response({
        #         "success":False,
        #         "message":"Not authorized to create user",
        #         "data":{
        #             "email":user.email
        #         }
        #     })




class LogoutView(APIView):

    def get(self, request):
        
        response = Response()
        response.delete_cookie('token') #delete the token
        
        response.data = {
            "success":True,
            'message': "success",
        }
        return response

