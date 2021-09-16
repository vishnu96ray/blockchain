from django.conf.urls import url
from django.urls import path
from accounts import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', views.accounts, name='accounts'),
    # url(r'^accounts/companydetails/$', companydetails, name='companydetails'),
    url(r'^accounts/change/password/$', changepassword, name='changepassword'),
    # url(r'^accounts/forgot/password/$', forgotpassword, name='forgotpassword'),
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


    url(r'^accounts/password_reset/$', auth_views.PasswordResetView.as_view(template_name='accounts/forgotpassword.html'), name="password_reset"),
    url(r'^accounts/_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='accounts/pw_sent.html'), name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/confirm.html'), name="password_reset_confirm"),
    url(r'^accounts/reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/pw_done.html'), name="password_reset_complete"),

]
