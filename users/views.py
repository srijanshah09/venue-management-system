from django.shortcuts import render
from rest_framework import viewsets, generics 
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from .models import User, Otp
from .utils import send_reset_password_email
from .utils import (
    validate_data, 
    register_user, 
    is_mobile,
    send_sms,
    get_tokens_for_user,
)

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

    def send_password_reset_email(self, request):
        email = request.data.get('email','')
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(request=request.domain)
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abs_url = 'http://localhost:8000' + relative_link 
            send_reset_password_email(email=email, link=abs_url)
        return Response(data = {'status': True, 'message':'Password reset link sent successfully.'}, status = status.HTTP_200_OK)

    def reset_password(self, request, uidb64, token):
        try:
            print(request.data, uidb64, token)
            password = request.data.get('password', None)
            if password and (len(password) > 7):
                id = smart_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id = int(id))
                if PasswordResetTokenGenerator().check_token(user,token):
                    user.set_password(password)
                    user.save()
                    return Response(data={"message":"Valid Credential, password reset successfully","uidb64":uidb64, "token":token,},status=status.HTTP_200_OK)
                else:
                    return Response(data={"message":"Invalid token"},status= status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(data={"message":"Invalid Password Provided"},status= status.HTTP_400_BAD_REQUEST )
        except DjangoUnicodeDecodeError as e:
            return Response(data={"message":"Invalid token"},status= status.HTTP_401_UNAUTHORIZED)
