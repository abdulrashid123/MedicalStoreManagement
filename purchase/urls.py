from django.urls import path,include
from rest_framework import routers
from purchase.views import *
router = routers.DefaultRouter()
router.register("buyer",BuyerViewSet,basename="buyer")
router.register("manufacture",ManufactureViewSet,basename="manufacture")
urlpatterns = [
    path('api/',include(router.urls)),
    path('test/',TestView.as_view())
]