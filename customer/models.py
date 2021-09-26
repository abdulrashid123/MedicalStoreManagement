from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from purchase.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The Email must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        print(user)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(username,password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

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


class Employee(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=255, unique=True, blank=True, null=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    joining_date=models.DateField(auto_now_add=True,blank=True,null=True)
    phone=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE,related_name="employee_store")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
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
    in_stock_total=models.IntegerField(blank=True,null=True)
    in_single_stock_total = models.IntegerField(blank=True,null=True)
    qty_in_strip=models.IntegerField(blank=True,null=True)
    free_strip = models.IntegerField(blank=True,null=True)
    category = models.CharField(max_length=200,blank=True,null=True)
    salt_name = models.CharField(max_length=255, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True) # tab,capsule,ml,gm
    description = models.CharField(max_length=255, blank=True, null=True) # silver simple blister
    schedule_drug = models.CharField(max_length=255, blank=True, null=True)
    buyer = models.ForeignKey(Buyer,blank=True, null=True, on_delete=models.CASCADE, related_name="buyer")
    manufacture = models.ForeignKey(ManuFacture, blank=True, null=True, on_delete=models.CASCADE, related_name="manufacture")

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
    employee = models.ForeignKey(Employee,blank=True, null=True, on_delete=models.CASCADE, related_name="worker")
    medicine =  models.ManyToManyField(Medicine,blank=True,related_name='med')
    qty=models.IntegerField()


    def get_total(self):
        return int(self.qty)

    def __str__(self):
        return f"{self.customer.name} == {self.get_total()}"
class MedicineTag(models.Model):
    tagName = models.CharField(max_length=200)
    medicine = models.ForeignKey(Medicine,blank=True, null=True, on_delete=models.CASCADE, related_name="medicine")


@receiver(pre_save,sender=Medicine)
def create_total_stock(sender, instance, *args, **kwargs):
    if instance.in_stock_total and instance.qty_in_strip:
        instance.in_single_stock_total = instance.in_stock_total * instance.qty_in_strip
