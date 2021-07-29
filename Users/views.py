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
                                "can_create_company":user.can_create_company,
                                "can_edit_company":user.can_edit_company,
                                "can_delete_company":user.can_delete_company,
                                "can_create_user":user.can_create_user,
                                "can_edit_user":user.can_edit_user,
                                "can_delete_user":user.can_delete_user,
                                "can_view_user":user.can_view_user,
                                "can_create_user_groups":user.can_create_user_groups,
                                "can_edit_user_groups":user.can_edit_user_groups,
                                "can_delete_user_groups":user.can_delete_user_groups,
                                "can_view_user_groups":user.can_view_user_groups
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
        
        if user.can_create_user:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": user.email
                })

            serializer.save()
            return Response({
                "success":True,
                "message":"User added successfully",
                "data":serializer.data
                })

        else:
            return Response({
                "success":False,
                "message":"Not authorized to create user",
                "data":{
                    "email":user.email
                }
            })


# API For editing user
# request : PUT
class EditUserView(APIView):
    def put(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_edit_user:
            selected_user = User.objects.get(id=id)
            serializer = UserSerializer(selected_user, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
            return Response({
                'success': True,
                'message': 'User Edited successfully'})
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit User',
                })

# API For deleting user
# request : DELETE
class DeleteUserView(APIView):
    def delete(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        if user.can_delete_user:
            selected_user = User.objects.get(id=id)
            selected_user.delete()
            return Response({
                'success': True,
                'message': 'User deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to User Company',
                })
# API For get all user
# request : GET
class GetUserView(APIView):
    def get(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_view_user:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
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
                'message': 'You are not allowed to View user Details',
            })

# API For getting particular user
# request : GET      
class DetailUserView(APIView):
    def get(self, request, id):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        if user.can_view_user:
            user_details = User.objects.get(id=id)
            serializer = UserSerializer(user_details)
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
                'message': 'You are not allowed to View User Details',
            })



class LogoutView(APIView):

    def get(self, request):
        
        response = Response()
        response.delete_cookie('token') #delete the token
        
        response.data = {
            "success":True,
            'message': "success",
        }
        return response

