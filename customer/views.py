from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from customer.models import *
from rest_framework import viewsets
from customer.serialiazers import *
from django.forms.models import model_to_dict
from django.http import JsonResponse
import time
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from django.db.models import Q
from rest_framework.authtoken.models import Token
# Create your views here.
from django.contrib.auth.models import User

class TokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,TokenAuthentication]

    def post(self, request):
        token = Token.objects.get_or_create(user=request.user)
        try:
            employee = get_object_or_404(EmployeeDetail,user=request.user)
            employee = employee.company.id
        except:
            employee = None
        return Response({'token':token[0].key,"isAdmin":request.user.is_superuser,"employeeId":request.user.id,"companyId":employee},status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=status.HTTP_200_OK)

class UsernameView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self,request):
        username = request.data.get('username')
        print(request.data)
        if User.objects.filter(username=username).exists():
            return Response({"exists":True},status=status.HTTP_200_OK)
        return Response({"exists":False},status=status.HTTP_200_OK)

class SearchMedicine(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,TokenAuthentication]

    def get(self,request):
        query = request.GET.get('searchQuery',None)
        asc = request.GET.get('asc',None)
        medicine_brands = request.GET.get('medicine_brand', None)
        product_form = request.GET.get('product_form', None)
        prescription_required = request.GET.get('prescription_required', None)
        obj = EmployeeDetail.objects.filter(user_id=request.user.id)

        age = request.GET.get('age', None)

        if query:
            data = Medicine.objects.filter(
                Q(medicine__tagName__startswith=query) | Q(name__startswith=query)).distinct()
            if obj:
                data = data.filter(Q(company=obj[0].company))
            if bool(asc) is True:
                data = data.order_by('-sell_price')
            if bool(asc) is False:
                data = data.order_by('sell_price')
            if medicine_brands:
                data = data.filter(Q(medicine_brand=medicine_brands))
            if product_form:
                data = data.filter(Q(product_form=product_form))
            if prescription_required:
                data = data.filter(Q(prescription_required=prescription_required))
            if age:
                data = data.filter(Q(age=age))
            if data:
                serializers = MedicineSerializer(data,many=True)
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response([],status=status.HTTP_200_OK)
        return Response({"error":True,"data":"no Query present"},status=status.HTTP_400_BAD_REQUEST)





class CompanyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] #permissions.IsAdminUser
    authentication_classes = [TokenAuthentication]

    def list(self,request):
        company=Company.objects.all()
        serializer=CompanySerializer(company,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict,status.HTTP_200_OK)

    def create(self,request):
        try:
            serializer= CompanySerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Data Save Successfully"}
            return Response(dict_response, status=status.HTTP_201_CREATED)
        except:
            dict_response={"error":True,"message":"Error During Saving Company Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, context={"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def update(self, request, pk=None):
        try:
            company = get_object_or_404(Company, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(dict_response, status=status.HTTP_200_OK)
        except:
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            company = get_object_or_404(Company, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(dict_response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response({"error": False, "message": "Successfully Deleted Company Data"})


class MedicineViewSet(viewsets.ViewSet):

    def list(self,request):
        medicine=Medicine.objects.all()
        serializer=MedicineSerializer(medicine,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Medicine List Data","data":serializer.data}
        return Response(response_dict)

    def create(self,request):
        try:
            tags = request.data.get('medicine_tags', None)
            in_stock_total = request.data.pop('in_stock_total',0)
            free_strip = request.data.pop('free_strip',0)
            serializer= MedicineSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            id = serializer.data.get('id')
            med = Medicine.objects.get(id=id)
            if tags:
                for each in tags:
                    MedicineTag.objects.create(medicine=med,tagName=each)
            med.in_stock_total += int(in_stock_total)
            med.free_strip += int(free_strip)
            med.in_single_stock_total += med.qty_in_strip * int(in_stock_total)
            med.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            dict_response={"error":True,"message":"Error During Saving Company Data"}
            return Response(dict_response)

    def update(self, request, pk=None):
        print(request.get_full_path())
        try:
            tags = request.data.get('medicine_tags', None)
            medicine = get_object_or_404(Medicine, pk=pk)
            serializer = MedicineSerializer(medicine, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()


            dict_response = {"error": False, "message": "Successfully Updated Medicine Data"}
            return Response(dict_response, status=status.HTTP_200_OK)
        except:
            dict_response = {"error": True, "message": "Error During Updating medicine Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            tags = request.data.get('medicine_tags', None)
            in_stock_total = request.data.pop('in_stock_total', 0)
            free_strip = request.data.pop('free_strip', 0)
            medicine= get_object_or_404(Medicine, pk=pk)
            serializer = MedicineSerializer(medicine,data=request.data,context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if tags:
                for each in tags:
                    MedicineTag.objects.create(medicine=medicine,tagName=each)
            medicine.in_stock_total += int(in_stock_total)
            medicine.free_strip += int(free_strip)
            medicine.in_single_stock_total += medicine.qty_in_strip * int(in_stock_total)
            medicine.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Updating medicine Data"}
            return Response(dict_response,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        print(request.get_full_path())
        medicine = get_object_or_404(Medicine, pk=pk)
        medicine.delete()
        return Response({"error": False, "message": "Successfully Deleted medicine Data"})


class CustomerViewSet(viewsets.ViewSet):

    def list(self,request):
        customer=Customer.objects.all()
        serializer=CustomerSerializer(customer,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict,status.HTTP_200_OK)

    def create(self,request):
        try:
            serializer= CustomerSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Data Save Successfully","data": serializer.data}
            return Response(dict_response, status=status.HTTP_201_CREATED)
        except:
            dict_response={"error":True,"message":"Error During Saving Company Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, context={"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def update(self, request, pk=None):
        try:
            customer = get_object_or_404(Customer, pk=pk)
            serializer = CustomerSerializer(customer, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(dict_response, status=status.HTTP_200_OK)
        except:
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            customer = get_object_or_404(Customer, pk=pk)
            serializer = CustomerSerializer(customer, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(dict_response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response({"error": False, "message": "Successfully Deleted Company Data"})


class EmployeeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def create(self,request):
        try:
            data = request.data
            date = data.get("date_joined",None)
            if date:
                data["date_joined"] = date+" 00:00:00"
            phone = data.pop('phone')
            company_id = data.pop('company')
            company = get_object_or_404(Company,pk=company_id)
            serializer= EmployeeSerializer(data=data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**data)
            if phone:
                u = EmployeeDetail.objects.create(user=user,phone=phone,company=company)
                u.save()
            else:
                u = EmployeeDetail.objects.create(user=user)
                u.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            dict_response={"error":True,"message":"Error During Saving Company Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        employee = get_object_or_404(User, pk=pk)
        serializer = EmployeeSerializer(employee, context={"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def update(self, request, pk=None):
        try:
            employee = get_object_or_404(User, pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            employee = get_object_or_404(User, pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(dict_response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        employee = get_object_or_404(User, pk=pk)
        employee.delete()
        return Response({"error": False, "message": "Successfully Deleted Company Data"})


class OrderViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def create(self,request):
        data = request.data
        medicines = data.pop('medicines')
        order = Order.objects.create(company_id=int(data.get('company')),employee_id=int(data.get('employee')))
        for each in medicines:
            id = each["id"]
            med = get_object_or_404(Medicine,pk=id)
            qty = each["qty"]
            if med.in_single_stock_total < qty:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
            else:
                order.medicine = med
                med.in_single_stock_total -= qty
                med.in_stock_total = (med.in_single_stock_total - qty)//med.qty_in_strip
                med.weight += 1
                med.save()
                order.save()
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = CustomerSerializer(order, context={"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def update(self, request, pk=None):
        try:
            order = get_object_or_404(Order, pk=pk)
            serializer = CustomerSerializer(order, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(dict_response, status=status.HTTP_200_OK)
        except:
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            order = get_object_or_404(Order, pk=pk)
            serializer = CustomerSerializer(order, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
            return Response(dict_response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Updating Company Data"}
            return Response(dict_response,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({"error": False, "message": "Successfully Deleted Company Data"})

class Sample(APIView):
    def post(self,request):
        print(request.data)
        return Response({"data":"success"},status=status.HTTP_200_OK)