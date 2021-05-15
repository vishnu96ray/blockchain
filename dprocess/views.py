import json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from accounts.models import *
from .models import ContactUs, Country, BusinessType



def home(request):
    template_name = "static/index.html"
    return render(request, template_name)

def aboutus(request):
    template_name = "static/aboutus.html"
    return render(request, template_name, {})


def privacy(request):
    template_name = "static/privacy.html"
    return render(request, template_name)


def terms(request):
    template_name = "static/terms.html"
    return render(request, template_name)

def delivery(request):
    template_name = "static/delivery.html"
    return render(request, template_name)


def site_mape(request):
    template_name = "static/site_mape.html"
    return render(request, template_name)



def affiliate(request):
    template_name = "static/affiliate.html"
    return render(request, template_name)



# def contactus(request):
#     if request.method == "POST":
#         try:
#             contact = ContactUs()
#             contact.name = request.POST.get('name')
#             contact.email = request.POST.get('email')
#             contact.message = request.POST.get('message')
#             contact.skypeid = request.POST.get('skypeid')
#             contact.mobile = int(request.POST.get('whatsapp_number'))
#             contact.country_id = int(request.POST.get('country'))
#             contact.status = 1
#             contact.save()
#             return HttpResponse(json.dumps(1), content_type="application/json")
#         except:
#             return HttpResponse(json.dumps(2), content_type="application/json")


# @login_required(login_url='/')
# def insite(request):
#     template_name = "myadmin/index.html"
#     return render(request, template_name)





