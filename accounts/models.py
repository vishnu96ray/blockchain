from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from dprocess.models import Country, BusinessType
from django.utils import timezone
from .choices import *


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userdetail")

    is_approved = models.BooleanField(default=True, null=True, blank=True)

    userstatus = models.IntegerField(choices=STATUS_CHOICE, default=1)
    
    applicant = models.CharField(max_length=100, null=True, blank=True)
    sodowo = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.BigIntegerField()

    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(default='18', null=True, blank=True)
    pan = models.CharField(max_length=10,unique=True, null=True, blank=True)
    joining_amt = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)

    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    
    address = models.TextField(null=True, blank=True)
    
    sponsor_name = models.CharField(max_length=100, null=True, blank=True)

    sponsor_mobile = models.CharField(max_length=100, null=True, blank=True)
    
    referral_code = models.CharField(max_length=100, null=True, blank=True)
    user_referral = models.CharField(max_length=100, null=True, blank=True)

    receipt_pic = models.FileField(upload_to='uploads/recepts',null=True, blank=True) 

    referred_by = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    level = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)
    
    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    def get_all_parents(self):
        parents = [self]
        if self.referred_by is not None:
            parent = self.referred_by
            parents.extend(parent.get_all_parents())
        return parents

class UserUsage(models.Model):
    userusage = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="usrusage")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    

class Payable(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_earning = models.FloatField(null=True, default=0.0)
    payable = models.FloatField(null=True, default=0.0)
    date = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.payable}'

class Holidays(models.Model):
    name = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    type = models.CharField(max_length=70, null=True)
    