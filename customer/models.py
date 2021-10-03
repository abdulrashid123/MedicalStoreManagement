from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from purchase.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.
from django.contrib.auth.models import User




class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Company(BaseModel):
    name=models.CharField(max_length=255,unique=True,default="owner")
    license_no=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    contact_no=models.CharField(max_length=255,blank=True,null=True)
    email=models.CharField(max_length=255,blank=True,null=True)
    description=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name
class EmployeeDetail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,blank=True,null=True)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, related_name="comp")


class Medicine(BaseModel):
    name=models.CharField(max_length=255,blank=True,null=True)
    medical_typ=models.CharField(max_length=255,blank=True,null=True)
    buy_price=models.CharField(max_length=255,blank=True,null=True)
    sell_price=models.CharField(max_length=255,blank=True,null=True)
    c_gst=models.CharField(max_length=255,blank=True,null=True)
    s_gst=models.CharField(max_length=255,blank=True,null=True)
    batch_no=models.CharField(max_length=255,blank=True,null=True)
    shelf_no=models.CharField(max_length=255,blank=True,null=True)
    expire_date=models.DateField(blank=True,null=True)
    mfg_date=models.DateField(blank=True,null=True)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, related_name="shop")
    in_stock_total=models.IntegerField(default=0)
    in_single_stock_total = models.IntegerField(default=0)
    qty_in_strip=models.IntegerField(default=0)
    free_strip =models.IntegerField(default=0)
    category = models.CharField(max_length=200,blank=True,null=True)
    salt_name = models.CharField(max_length=255, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True) # tab,capsule,ml,gm
    description = models.CharField(max_length=255, blank=True, null=True) # silver simple blister
    schedule_drug = models.CharField(max_length=255, blank=True, null=True)
    buyer = models.CharField(max_length=255, blank=True, null=True)
    manufacture = models.CharField(max_length=255, blank=True, null=True)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Customer(BaseModel):
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=255,blank=True,null=True)
    contact=models.CharField(max_length=255,blank=True,null=True)
    doctor_name = models.CharField(max_length=255,blank=True,null=True)
    doctor_address = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name

class Order(BaseModel):
    customer = models.ForeignKey(Customer,blank=True,null=True,on_delete=models.CASCADE,related_name="buyer")
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, related_name="store")
    employee = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE, related_name="worker")
    medicine =  models.ManyToManyField(Medicine,blank=True,related_name='med')
    qty=models.IntegerField()


    def get_total(self):
        return int(self.qty)

    def __str__(self):
        return f"{self.customer.name} == {self.get_total()}"
class MedicineTag(models.Model):
    tagName = models.CharField(max_length=200)
    medicine = models.ForeignKey(Medicine,blank=True, null=True, on_delete=models.CASCADE, related_name="medicine")



