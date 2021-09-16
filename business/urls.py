from django.urls import path
from business import views

urlpatterns = [
    path('insite/', views.business, name='insite'),
    path('insite/userprofile/', views.userprofile, name='profile'),
    path('insite/update_holidays/', views.update_holidays, name='update_holidays'),
    path('reinvest/', views.reinvest, name='reinvest'),
    path('payables/', views.payable, name='payable'),
    path('activate_payables/<str:pk>/', views.activate_payable, name='activate_payable'),
]
