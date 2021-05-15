from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', home, name="homepage"),
    url(r'^about-us/$', aboutus, name="aboutus"),
    url(r'^privacy/$', privacy, name="privacy"),
    url(r'^terms/$', terms, name="terms"),
    url(r'^delivery/$', delivery, name="delivery"),
    url(r'^site_mape/$', site_mape, name="site_mape"),
    url(r'^affiliate/$', affiliate, name="affiliate"),
   
    # url(r'^contactus/$', contactus, name="contactus"),


]
