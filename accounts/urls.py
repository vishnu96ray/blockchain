from django.conf.urls import url
from django.urls import path
from accounts import views
from .views import *

urlpatterns = [
    path('accounts/', views.accounts, name='accounts'),
    # url(r'^accounts/companydetails/$', companydetails, name='companydetails'),
    url(r'^accounts/change/password/$', changepassword, name='changepassword'),
    url(r'^accounts/forgot/password/$', forgotpassword, name='forgotpassword'),
    url(r'^accounts/register/user/$', site_user_registration, name='site-user-registration'),
    url(r'^accounts/signin/$', login_site, name='login'),
    url(r'^accounts/signin/(?P<username>.+)/$', admin_login, name='admin_login'),
    url(r'^accounts/logout/$', auth_logout, name='auth-logout'),
    url(r'^insite/accounts/usage/$', accounts_usage, name="accounts_usage"),
    # url(r'^insite/api/$', TemplateView.as_view(template_name='myadmin/my_api_credentials.html'), name="api_details"),
    # url(r'^insite/api/(?P<status>.+)/$', api_access, name="api_access"),
    url(r'^accounts/lock_screen/$', lock_screen, name="lock_screen"),
    # url(r'^accounts/calculateProfit/(?P<id>\d+)$', calculateProfit, name="calculateProfit"),
    # url(r'^accounts/ReferralDetails/(?P<referral>[\w-]+)$', ReferralDetails, name="ReferralDetails"),

]
