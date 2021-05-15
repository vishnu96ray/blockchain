from django.conf.urls import url
from . import views
from .views import *


urlpatterns = [
    url(r'^$', views.dprocess, name="dprocess"),
    url(r'^about-us/$', aboutus, name="aboutus"),
    url(r'^privacy/$', privacy, name="privacy"),
    url(r'^terms/$', terms, name="terms"),
    url(r'^delivery/$', delivery, name="delivery"),
    url(r'^site_mape/$', site_mape, name="site_mape"),
    url(r'^affiliate/$', affiliate, name="affiliate"),
   
    # url(r'^contactus/$', contactus, name="contactus"),


]
