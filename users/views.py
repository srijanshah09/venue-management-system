from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class UserAuthView(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = ()

    def register(self,request):
        try:
            data = request.data
            print(data)
            return Response(
                data = {'status': True, 'message': 'ALL OK',},
                status = status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data = {'status': False, 'message': str(e),},
                status = status.HTTP_400_BAD_REQUEST,
            )
