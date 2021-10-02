from django.shortcuts import render
from Users.models import User
from Company.models import voucher_type
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, timedelta
from django.http.response import HttpResponse
from django.http import JsonResponse
import jwt
# Create your views here.

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


# API For getting all voucher type
# request : GET
# endpoint : get-vouhcers
class GetVouchers(APIView):
    def get(self, request):
        payload = verify_token(request)
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        all_voucher = voucher_type.objects.all()
        data = []
        for i in all_voucher:
            temp = {}
            temp.update({"voucher_type": i.voucher_name})
            if i.auto_numbering:
                temp.update({"auto_numbering": True})
                temp.update({"voucher_no": i.prefix})
            else:
                temp.update({"auto_numbering": False})
                temp.update({"voucher_no": ""})
            data.append(temp)
        return Response({
            'success': True,
            'message':'',
            'data': data
            })




      
