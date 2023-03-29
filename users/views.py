from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework import status
from rest_framework.response import Response
from .utils import (
    validate_data, 
    register_user, 
    is_mobile,
    generate_otp,
    send_sms,
    get_tokens_for_user,
)
from .models import User, Otp

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
        try:
            mobile = request.data.get('mobile',None)
            if mobile:
                mobile = mobile.strip()
                if is_mobile(mobile):
                    if User.objects.filter(mobile=mobile).exists():
                        send_sms(mobile)
                        return Response(
                            data = {'status': True, 'message': str(mobile)},
                            status = status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            data = {'status' : False, 'message': 'No account found!',},
                            status = status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        data = {'status' : False, 'message': 'Invalid mobile number',},
                        status = status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    data = {'status' : False, 'message': 'Invalid mobile number',},
                    status = status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                data = { 'status': False, 'message': str(e),},
                status = status.HTTP_400_BAD_REQUEST,
            )



    def verify_otp(self, request):
        """LOGIN with OTP"""
        try:
            mobile = request.data.get('mobile')
            otp = request.data.get('otp')
            if mobile and otp:
                mobile = mobile.strip()
                otp = otp.strip()
                if Otp.objects.filter(mobile=mobile).exists():
                    instance = Otp.objects.filter(mobile=mobile).last()
                    if instance.otp == int(otp):
                        user = User.objects.get(mobile=mobile)
                        token = get_tokens_for_user(user)
                        return Response(
                            data = {'status': True, 'message':'Correct OTP', 'token':token,},
                            status = status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            data = {'status': False, 'message': 'Invalid OTP'},
                            status = status.HTTP_200_OK
                        )
                else:
                    return Response(
                        data = {'status':False, 'message': 'Invalid Data'},
                        status = status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    data = {'status':False, 'message': 'OTP or Mobile is None'},
                    status = status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                data = {'status': False, 'message': str(e),},
                status = status.HTTP_400_BAD_REQUEST,
            )