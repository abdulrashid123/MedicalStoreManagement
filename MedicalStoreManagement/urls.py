"""MedicalStoreManagment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from customer.views import Sample
from rest_framework.authtoken import views
from customer.views import SearchMedicine,TokenView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', TokenView.as_view()),
    path('',include(('customer.urls','customer'),namespace='customer')),
    path('',include(('purchase.urls','purchase'),namespace='purchase')),
    path('sample/',Sample.as_view()),
    path('search/',SearchMedicine.as_view())
]
