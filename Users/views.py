""" 
Developed by Techlace 
updated on : 31-07-2021
Status : {
    "API": done, 
    "backend testing : done, 
    "documentation: done,
    "postman API added" : done,
    }
"""

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import jwt, datetime
from django.http import JsonResponse
from .serializers import *


# Function to verify the accessToken
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

# Function getting error from serializer
def get_error(serializerErr):

    err = ''
    for i in serializerErr:
        err = serializerErr[i][0]
        break    
    return err


class VerifyUser(APIView):
    def get(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        return Response({
                        "success":True,
                        "message":"User logged in successfully",
                        "data":
                            {
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
                        })
    


# Login API 
# Request : POST
# Endpoint : login
class LoginView(APIView):


    def post(self, request):

        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        # Check if user exists or not
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

        # Validate password
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

        #generating token
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8') 
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


# API for creating a user
# Request : POST
# Endpoint : add-user
class AddUserView(APIView):


    def post(self, request):

        # Verify token i.e checks user is authenticated or not
        payload = verify_token(request)

        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        # permission : If user can create another user
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


# API for editing user
# Request : PUT
# Endpoint : edit-user/<int:id>
class EditUserView(APIView):


    def put(self, request, id):
        
        payload = verify_token(request)

        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        # permission : If user can edit another user
        if user.can_edit_user:
            
            # Fetch user data from the database with a specific id = "id"
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


# API for deleting user
# Request : DELETE
# Endpoint : delete-user/<int:id>
class DeleteUserView(APIView):


    def delete(self, request, id):

        payload = verify_token(request)
        
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        # permission : if user can delete another user 
        if user.can_delete_user:
            
            # Fetch details of user with a specific id = "id"
            selected_user = User.objects.get(id=id)
            # Delete fetched user
            selected_user.delete()

            return Response({
                'success': True,
                'message': 'User deleted Successfully',
                })
        
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Delete User Company',
                })


# API for retrieving all user
# Request : GET
# Endpoint : get-users
class GetUserView(APIView):
    
    def get(self, request):
    
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
    
        # permission : If user can view other user
        if user.can_view_user:
            
            # Fetch user details of all existing users in database
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


# API for retrieving particular user
# Request : GET    
# Endpoint : get-users/<int:id>
class DetailUserView(APIView):
    
    
    def get(self, request, id):
    
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
    
        # permission : If user can view another user
        if user.can_view_user:

            # Fetch details of user with a specific id = "id"
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


# API For creating a user group
# request : POST  
# Endpoint : add-user-group
class AddUserGroup(APIView):
    

     def post(self, request):
    
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        # Permission : If user is allowed to create a user group
        if user.can_create_user_groups:

            serializer = UserGroupSerializer(data=request.data)

            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": user.email
                })

            serializer.save()
    
            return Response({
                "success":True,
                "message":"User Groups added successfully",
                "data":serializer.data
                })

        else:
            return Response({
                "success":False,
                "message":"Not authorized to create User Groups",
                "data":{
                    "email":user.email
                }
            })


# API For updating a user group
# Request : PUT
# Endpoint : edit-user-group/<int:id>
class EditUserGroup(APIView):
    
    
    def put(self, request, id):
    
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        # Permission : If user is allowed to edit a user group
        if user.can_edit_user_groups:
            
            # Fetch user group details with a specific is = "id"
            selected_group = user_group.objects.get(id=id)
            serializer = UserGroupSerializer(selected_group, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
    
            return Response({
                'success': True,
                'message': 'User Group Edited successfully'})
    
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit User Group',
                })


# API For deleting a user group
# Request : DELETE
# Endpoint : delete-user-group/<int:id>
class DeleteUserGroup(APIView):
    
    
    def delete(self, request, id):
    
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        # Permission : If user is allowed to delete a user group
        if user.can_delete_user_groups:

            # Fetch user group with a specific id = "id"
            selected_group = user_group.objects.get(id=id)
            selected_group.delete()

            return Response({
                'success': True,
                'message': 'User Group deleted Successfully',
                })
    
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Delete User Group',
                })


# API For retrieving a user group
# request : GET
# endpoint : get-user-group
class GetUserGroup(APIView):
    def get(self, request):
        # verify token for authorization
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
    
        # perimission type : can view user groups
        if user.can_view_user_groups:
            # Query : Get all user group data
            user_groups = user_group.objects.all()
            serializer = UserGroupSerializer(user_groups, many=True)
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
                'message': 'You are not allowed to View User Groups',
            })


# API For creating user rights
# request : POST
# endpoint : add-user-right
class AddUserRight(APIView):


    def post(self, request):

        # verify token for authorization
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
    
        # Permission type : can create user
        if user.can_create_user:
            serializer = UserRightSerializer(data=request.data)

            # check serializer validation
            if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": user.email
                })

            serializer.save()
    
            return Response({
                "success":True,
                "message":"User Rights added successfully",
                "data":serializer.data
                })

        else:
            return Response({
                "success":False,
                "message":"Not authorized to Add User Rights",
                "data":{
                    "email":user.email
                }
            })


# API For updating user rights
# request : PUT
# endpoint : edit-user-right/<int:id>
class EditUserRight(APIView):
    def put(self, request, id):
        # verify user token for authorization
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload

        # Permission type : can edit user
        if user.can_edit_user:

            # Query : To fetch user right data by parameter id
            selected_group = user_right.objects.get(id=id)
            serializer = UserRightSerializer(selected_group, data=request.data)

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': get_error(serializer.errors),
                    })
                    
            serializer.save()
    
            return Response({
                'success': True,
                'message': 'User Rights Edited successfully'})
    
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to edit User Rights',
                })


# API For deleting user rights
# request : DELETE
# endpoint : delete-user-right/<int:id>
class DeleteUserRight(APIView):
    def delete(self, request, id):
        # verify user is authorized or not
        payload = verify_token(request)
    
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        # Permission type : can delete company
        if user.can_delete_company:
            # Fetch data using id to delete user right 
            user_rights = user_right.objects.get(id=id)
            user_rights.delete()
            return Response({
                'success': True,
                'message': 'User Right deleted Successfully',
                })
        else:
            return Response({
                'success': False,
                'message': 'You are not allowed to Delete User Right',
                })


# API For retrieving a user group
# request : GET
# endpoint : get-user-right
class GetUserRight(APIView):
    def get(self, request):

        # verify token of authorized user
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        # permission : can view user
        if user.can_view_user:

            # Fetch all user rights data
            user_groups = user_right.objects.all()
            serializer = GetUserRightSerializer(user_groups, many=True)
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
                'message': 'You are not allowed to View User Right',
            })
            

# Logout API
# request : GET
# endpoint : logout
class LogoutView(APIView):

    def get(self, request):
        response = Response()
        response.delete_cookie('token') #delete the token
        
        response.data = {
            "success":True,
            'message': "success",
        }
        return response

