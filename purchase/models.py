from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Stock(BaseModel):
    name = models.CharField(max_length=200)
    mobile_no = models.CharField(validators=[
        RegexValidator(
            regex='[1-9]{1}[0-9]{9}',
            message='Number should be 10 digit',
            code='invalid_number'
        ),
    ], max_length=10, blank=True, null=True)
    address = models.TextField(blank=True,null=True)
    gst_no = models.CharField(max_length=200,blank=True,null=True)
    pan_no = models.CharField(max_length=200,blank=True,null=True)


    def __str__(self):
        return self.name

#Buyer
#name,short name, mr name mr no
class Buyer(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    short_name = models.CharField(max_length=200,blank=True,null=True)
    mr_name = models.CharField(max_length=200,blank=True,null=True)
    mr_no = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.name



class ManuFacture(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    short_name = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.name



class Billing(BaseModel):
    stock = models.ForeignKey(Stock,blank=True,null=True,on_delete=models.CASCADE,related_name="stock")
    payment_method = models.CharField(max_length=200,blank=True,null=True)
    invoice_number = models.CharField(max_length=200,blank=True,null=True)
    discount = models.IntegerField(blank=True,null=True)


@receiver(pre_save,sender=Buyer)
def change_short_name(sender, instance, *args, **kwargs):
    instance.short_name = instance.name[:2].upper()

@receiver(pre_save,sender=ManuFacture)
def my_callback(sender, instance, *args, **kwargs):
    instance.short_name = instance.name[:2].upper()




