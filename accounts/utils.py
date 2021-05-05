import decimal
from django.contrib.auth.models import User
from accounts.models import UserUsage, UserProfile
#from product.models import Product
from .choices import *


def authenticate_api(username, key):
    """
    If the given credentials are valid, return a User object.
    """
    try:

        userprofile = UserProfile.objects.get(user__username=username, key=key)
        return userprofile.user
    except UserProfile.DoesNotExist:
        return None
    except:
        return None


def site_usage(rows, product_id, userdetail):
    product = Product.objects.get(pk=product_id)
    price = rows * (product.price) / product.quantity
    if price < 0.001:
        price = decimal.Decimal('0.001')
    usage = UserUsage(userusage=userdetail, product=product, quantity=rows, price=price)
    usage.save()
    userdetail.remaining_amount -= price
    userdetail.used_amount += price
    userdetail.save()


def check_credit(rows, product_id, userdetail):
    product = Product.objects.get(pk=product_id)
    price = rows * (product.price) / product.quantity
    if price < 0.001:
        price = decimal.Decimal('0.001')
    if userdetail.remaining_amount < price:
        return True
    return False


def get_parentuser(user):
    if user.userdetail.parentuser is None:
         parentuser = user
         return parentuser
    else:
        parentuser = user.userdetail.parentuser
        return parentuser

def get_permission_based_subuser(subuser, role, user):
    if user.userdetail.parentuser is None:
        return subuser
    else:
        if role == 1:
            subuser = subuser.exclude(userrole=1)
        elif role == 2:
            subuser = subuser.exclude(userrole= 1)
            subuser = subuser.exclude(userrole=2)
        elif role == 3:
            subuser = subuser.exclude(userrole= 1)
            subuser = subuser.exclude(userrole=2)
            subuser = subuser.exclude(userrole=3)
        return subuser

def get_role(user):
    if user.userdetail.parentuser is None:
        return USER_ROLE
    else:
        if user.userdetail.userrole == 1:
            role = USER_ROLE[1:]
            return role
        elif user.userdetail.userrole == 2:
            role = USER_ROLE[2:]
            return role


def get_subuseruser_list(user):
    parentuser = get_parentuser(user)
    subuser = UserProfile.objects.filter(parentuser=parentuser, user__is_active=True)
    role = user.userdetail.userrole
    subuser = get_permission_based_subuser(subuser, role, user)
    return subuser

def get_user_list(user):
    parentuser = get_parentuser(user)
    subuser = UserProfile.objects.filter(parentuser=parentuser, user__is_active=True)
    subuser = [userprofile.user for userprofile in subuser]
    subuser.append(parentuser)
    return subuser
