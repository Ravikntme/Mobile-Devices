import logging
import json
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status, views
from rest_framework.filters import OrderingFilter
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from .serializers import MobileSerializer
from .models import *

# Logger variables to be used for logging
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')

# APi to Aunthenticate User
# Here basic Authentication 
class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    # request.user will be a Django User instance.
    # request.auth will be None.
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get(self, request, format=None):
        
        content = {
            
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)


# Api to add Mobile devices for authenticated User only
class MobileDevicesCreate(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            response = {'data':[], 'message':'Api Failed', 'status':'failed'}
            try:
                data = json.loads(request.body)
            except:
                data = request.data
            brand = data.get('brand')
            model = data.get('model')
            colour = data.get('colour')
            price = data.get('price')
            mobile_devices = Mobile.objects.create(brand = brand, model = model, colour = colour, price = price)
            mobile_serialize = MobileSerializer(mobile_devices)
            response['data'] = mobile_serialize.data
            response['message'] = "Mobile devices details added successfully"
            response['status'] = "Success"
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(e, exc_info=True)
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)


# Api to delete Mobile devices for authenticated user only
class MobileDevicesDelete(APIView):
    
    def delete(self,request):
        try:
            response = {'data':[], 'message':'Api Failed', 'status':'failed'}
            try:
                data = json.loads(request.body)
            except:
                data = request.data
            id = data.get('id')
            del_obj = Mobile.objects.get(id = id)
            del_obj.delete()
            response['message'] = f'{del_obj.brand} {del_obj.model} get deleted now'
            mobile_obj = Mobile.objects.all()
            response['data'] = MobileSerializer(mobile_obj, many=True).data
            response['status'] = "Success"
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(e, exc_info=True)
            return Response(response,status=status.HTTP_204_NO_CONTENT)

# API to List all Mobiles with brand, model,colour
class MobilewithFilter(APIView):

    def get(self,request):
        try:
            response = {'data': [], 'message': 'API Failed', 'status': 'failed'}
            try:
                data = json.loads(request.body)
            except:
                data = request.data
            q = data.get('filter_by')
            mobile_query = Mobile.objects.all()
            mobile_obj = mobile_query.filter(Q(brand = q)|Q(model = q)|Q(colour = q))
            mobile_data = MobileSerializer(mobile_obj,many=True)
            response['data'] = mobile_data.data
            response['message'] = "Mobile list with filter Successfully fetched"
            response['status'] = 'Success'
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(e, exc_info=True)
            return Response(response, status=status.HTTP_204_NO_CONTENT)


# API to list all Mobile
class MobileList(APIView):

    def get(self,request):
        try:
            response = {'data': [], 'message': 'API Failed', 'status': 'failed'}
            mobile_query = Mobile.objects.all().order_by('id')
            mobile_data = MobileSerializer(mobile_query, many = True)
            response['data'] = mobile_data.data
            response['message'] = "Mobile list Successfully fetched"
            response['status'] = 'Success'
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(e, exc_info=True)
            return Response(response, status=status.HTTP_204_NO_CONTENT)


# Api to list all Mobile in Min and Max Price Range       
class MobileListwithPriceRange(APIView):

    def get(self,request):
        try:
            response = {'data': [], 'message': 'API Failed', 'status': 'failed'}
            try:
                data = json.loads(request.body)
            except:
                data = request.data
            min_price = data.get('price_min')
            max_price = data.get('price_max')
            mobile_query = Mobile.objects.all().filter(price__gte = min_price, price__lte = max_price)
            mobile_data = MobileSerializer(mobile_query, many = True)
            response['data'] = mobile_data.data
            response['message'] = "Mobile list in Price Range Successfully fetched"
            response['status'] = 'Success'
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(e, exc_info=True)
            return Response(response, status=status.HTTP_204_NO_CONTENT)


# Api to list all mobile devices in ascending or descending order according to user request
class MobilewListinOrder(ListAPIView):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    filter_backends = [OrderingFilter]
    