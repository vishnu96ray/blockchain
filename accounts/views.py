import json
import binascii
import os
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import *
from .choices import *
from dprocess.decorators import login_required_ajax
from .models import *
from .service import *



def site_user_registration(request):
    if request.method == "POST":
        ref = referral()
        upass = usesrpass()
        print(upass,11212121)
        username = ref
        password = upass
        user_referral = ref
        applicant = request.POST.get("applicant")
        sodowo    = request.POST.get("sodowo")
        gender    = request.POST.get("gender")
        email     = request.POST.get("email")
        mobile    = request.POST.get('mobile')
        dob       = request.POST.get("dob")  
        age       = request.POST.get("age")  
        pan       = request.POST.get("pan")
        joining_amt = request.POST.get("joining_amt")
          
        district  = request.POST.get("district")  
        city      = request.POST.get("city")
        state     = request.POST.get("state")  
        pincode   = request.POST.get("pincode")
        address   = request.POST.get("address", "")
        sponsor_name = request.POST.get("sponsor_name")
        try:
            sponsor_mobile = request.POST.get("sponsor_mobile", "")
        except:
            print("Mobile Number not entered!")
        referral_code = request.POST.get("referral_code")
        email = email.lower()
        cus = User.objects.filter(Q(email=email) | Q(username=username))
        if cus:
            return HttpResponse(json.dumps(2), content_type="application/json")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            # user.is_staff=True
            user.is_active = True
            user.save()
            profileinfo = UserProfile(user=user, user_referral=user_referral, applicant=applicant, sodowo=sodowo, gender=gender, city=city,district=district, state=state, pincode=pincode, dob=dob, age=age, pan=pan, address=address,joining_amt=joining_amt, sponsor_name=sponsor_name, sponsor_mobile=sponsor_mobile, referral_code=referral_code, mobile=mobile, userstatus=1,)
            print(referral_code)

            if referral_code is None:
                profileinfo.level = 1
            else:
                referred_by = UserProfile.objects.get(user_referral=referral_code)
                profileinfo.referred_by = referred_by

                profileinfo.level = int(referred_by.level) + 1
            profileinfo.save()
            # username(referralID) and password send to the customer registered Number
            user = user.username
            userauthsend(mobile,user,username,password)
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return redirect("/")
    else:
        template_name = 'accounts/user_register.html'
        return render(request, template_name)


def login_site(request):
    if request.method == "POST":
        cus = None
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            cus = User.objects.get(username=username)
        except:
            try:
                cus = User.objects.get(email=username)
            except:
                return HttpResponseRedirect("/accounts/signin/?msg=Username is not correct.Please fill correct one.")
        user = authenticate(username=cus.username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect("/insite/")
        else:
            return HttpResponseRedirect("/accounts/signin/?msg=Password is not correct.Please fill correct one.")
    else:
        template_name = 'accounts/login.html'
        return render(request, template_name, {})


def changepassword(request):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(3), content_type="application/json")
    password = request.POST.get('new_password')
    try:
        user = request.user
        user.set_password(password)
        user.save()
    except:
        return HttpResponse(json.dumps(2), content_type="application/json")

    return HttpResponse(json.dumps(1), content_type="application/json")

@login_required
def forgotpassword(request):
    template_name = 'accounts/forgotpassword.html'
    msg = None
    if request.method == "POST":
        sourcemail = request.POST.get('email')
        username = request.POST.get('username')
        asd = str(sourcemail)
        try:
            obj = User.objects.get(email=asd, username=username)
            # password=obj.userdetail.mobile
            # password= ''.join(random.choice(string.ascii_letters) for x in range(6))
            # obj.set_password(password)
            # obj.save()
            # templatename="mail/forgot-mailer.html"
            # c={'user':obj,}
            # message = loader.render_to_string(templatename, c)
            # send_mail('Instructions for changing your MailCleaners Password',message,'"MailCleaners Account" <admin@mailcleaners.org>',[sourcemail],fail_silently=False,html_message=message)
            msg = "Please <a href='/accounts/signin/%s/'>click here</a> for login on your account. After login please visit profile page to change your password for further use." % (
                obj.username)
        except Exception as e:
            return render(request, template_name,
                          {'msg': "We have not any user associated with that username and email id."})
        return render(request, template_name, {'msg': msg})
    return render(request, template_name, {})


@login_required_ajax
def accounts(request):
    template_name = 'myadmin/profile.html'
    if request.method == "POST":
        try:
            name = request.POST.get('first_name')
            mobile = request.POST.get('mobile')
            county_id = request.POST.get('country_detail')
            business_type_id = request.POST.get('business_type')
            request.user.first_name = name
            request.user.save()
            request.user.userdetail.mobile = mobile
            request.user.userdetail.country_detail_id = county_id
            request.user.userdetail.business_type_id = business_type_id
            request.user.userdetail.save()
            return HttpResponse(json.dumps(1), content_type="application/json")
        except:
            return HttpResponse(json.dumps(2), content_type="application/json")
    return render(request, template_name,
                  {'country_list': Country.objects.all(), 'business_type': BusinessType.objects.all()})


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def companydetails(request):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(3), content_type="application/json")
    if request.method == "POST":
        try:
            company = request.POST.get('company')
            website = request.POST.get('website')
            address = request.POST.get('address')
            request.user.userdetail.company = company
            request.user.userdetail.website = website
            request.user.userdetail.address = address
            request.user.userdetail.save()
            return HttpResponse(json.dumps(1), content_type="application/json")
        except:
            return HttpResponse(json.dumps(2), content_type="application/json")

    return HttpResponse(json.dumps(2), content_type="application/json")


def admin_login(request, username):
    user = User.objects.get(username=username)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect("/insite/")


@login_required(login_url='/')
def accounts_usage(request):
    fromdate = request.GET.get('fromdate', None)
    todate = request.GET.get('todate', None)
    template_name = "accounts/usage.html"
    usage = UserUsage.objects.filter(active=True, userusage__user=request.user).order_by("-date")
    if fromdate and todate:
        fromdate = fromdate + " 00:00"
        todate = todate + " 23:59"
        usage = usage.filter(date__range=[fromdate, todate])
    total = usage.aggregate(Sum('price'))
    paginator = Paginator(usage, 1000)
    page = request.GET.get('page')
    try:
        usage = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        usage = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        usage = paginator.page(paginator.num_pages)

    return render(request, template_name, {'usage': usage, 'total': total.get("price__sum")})


def lock_screen(request):
    template_name = 'accounts/lockscreen.html'
    return render(request, template_name)


def calculateProfit(request, id):
    user = UserProfile.objects.filter(id=id)
    if user.exists():
        profit = []
        referral_code = user[0].referral_code
        for i in range(0, 5):
            if(referral_code is not None):
                referredBy = UserProfile.objects.filter(
                    user_referral=referral_code)
                percentage = 5/2**i
                profitAmount = float(user[0].joining_amt)*percentage/100
                profit.append((referredBy[0], percentage, profitAmount))
                referral_code = referredBy[0].referral_code
            else:
                break
        print(profit)
    return "User not found"


# def ReferralDetails(request, referral):
#     users = UserProfile.objects.filter(referral_code=referral)
#     print(users)
#     return HttpResponse("success")

