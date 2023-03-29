from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework import status
from rest_framework.response import Response
from .utils import validate_data, register_user
from .models import User

# Create your views here.
class UserAuthView(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = ()

    def register(self,request):
        try:
            data = request.data
            print(data)
            validate, msg = validate_data(data)
            if validate:
                user = register_user(data)
                if not user:
                    return Response(
                        data={'status': False, 'message': "User already exists"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
 
                return Response(
                    data = {'status': validate, 'message': msg,},
                    status = status.HTTP_200_OK,
                )
            else:
                return Response(
                    data = {'status': validate, 'message': msg,},
                    status = status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                data = {'status': False, 'message': str(e),},
                status = status.HTTP_400_BAD_REQUEST,
            )

    def send_otp(self, request):
        """SEND OTP"""
        mobile = request.data.get('mobile',None)
        if mobile:
            mobile = mobile.strip()
            if User.objects.filter(mobile=mobile).exists():
                pass

    def verify_otp(self, request):
        """LOGIN with OTP"""
        pass