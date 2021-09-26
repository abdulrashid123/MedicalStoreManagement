from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from .models import *
from .serializers import *
import time
from rest_framework.authtoken.models import Token

# Create your views here.
class BuyerViewSet(viewsets.ViewSet):

    def list(self,request):
        buyer=Buyer.objects.all()
        serializer=BuyerSerializer(buyer,many=True,context={"request":request})
        response_dict={"error":False,"data":serializer.data}
        return Response(response_dict,status.HTTP_200_OK)

    def create(self,request):
        try:
            serializer= BuyerSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"data":serializer.data}
            return Response(dict_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            dict_response={"error":True,"message":"Error During Saving Buyer Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)
    #
    def retrieve(self, request, pk=None):
        buyer = get_object_or_404(Buyer, pk=pk)
        serializer = BuyerSerializer(buyer, context={"request": request})
        response_dict = {"error": False, "data": serializer.data}
        return Response(response_dict)
    #
    def update(self, request, pk=None):
        try:
            buyer = get_object_or_404(Buyer, pk=pk)
            serializer = BuyerSerializer(buyer, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "data":serializer.data}
            return Response(dict_response, status=status.HTTP_200_OK)
        except:
            dict_response = {"error": True, "message": "Error During Updating Buyer Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)
    #
    def partial_update(self, request, pk=None):
        try:
            buyer = get_object_or_404(Buyer, pk=pk)
            serializer = BuyerSerializer(buyer, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "data": serializer.data}
            return Response(dict_response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Updating buyer Data"}
            return Response(dict_response,status=status.HTTP_400_BAD_REQUEST)
    #
    def destroy(self, request, pk=None):
        buyer = get_object_or_404(Buyer, pk=pk)
        buyer.delete()
        return Response({"error": False, "message": "Successfully Deleted Buyer Data"})


class ManufactureViewSet(viewsets.ViewSet):

    def list(self,request):
        manufacture=ManuFacture.objects.all()
        serializer=ManufactureSerializer(manufacture,many=True,context={"request":request})
        response_dict={"error":False,"data":serializer.data}
        return Response(response_dict,status.HTTP_200_OK)

    def create(self,request):
        try:
            serializer= ManufactureSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"data":serializer.data}
            return Response(dict_response, status=status.HTTP_201_CREATED)
        except:
            dict_response={"error":True,"message":"Error During Saving manufacture Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)
    #
    def retrieve(self, request, pk=None):
        manufacture = get_object_or_404(ManuFacture, pk=pk)
        serializer = ManufactureSerializer(manufacture, context={"request": request})
        response_dict = {"error": False, "data": serializer.data}
        return Response(response_dict)
    #
    def update(self, request, pk=None):
        try:
            manufacture = get_object_or_404(ManuFacture, pk=pk)
            serializer = ManufactureSerializer(manufacture, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "data":serializer.data}
            return Response(dict_response, status=status.HTTP_200_OK)
        except:
            dict_response = {"error": True, "message": "Error During Updating manufacture Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)
    #
    def partial_update(self, request, pk=None):
        try:
            manufacture = get_object_or_404(ManuFacture, pk=pk)
            serializer = ManufactureSerializer(manufacture, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "data": serializer.data}
            return Response(dict_response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Updating manufacture Data"}
            return Response(dict_response,status=status.HTTP_400_BAD_REQUEST)
    #
    def destroy(self, request, pk=None):
        manufacture = get_object_or_404(ManuFacture, pk=pk)
        manufacture.delete()
        return Response({"error": False, "message": "Successfully Deleted Buyer Data"})

class TestView(APIView):
    permission_classes = [IsAuthenticated] #permissions.IsAdminUser
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        obj = Token.objects.get(user=request.user)
        obj.delete()
        return Response({"data":"success"})
