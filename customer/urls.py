from django.urls import path,include
from rest_framework import routers
from customer.views import *

router = routers.DefaultRouter()
router.register("company",CompanyViewSet,basename="company")
router.register("medicine",MedicineViewSet,basename="medicine")
router.register("customer",CustomerViewSet,basename="customer")
router.register("employee",EmployeeViewSet,basename="employee")



urlpatterns = [
    path('api/',include(router.urls))
]