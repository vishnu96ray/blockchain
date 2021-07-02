from django.contrib import admin
from django.utils.html import format_html
from .models import *
from import_export.admin import ImportExportModelAdmin


class UserProfileAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'applicant', 'sodowo','gender','dob','age','pan','joining_amt','district','city','state','pincode','address',
        'sponsor_name','sponsor_mobile', 'user_referral', 'referral_code','receipt_pic', 'referred_by', 'level',
        'user_email', 'username', 'mobile', 'first_name', 'last_name', 'last_login', 'date_joined', 'address',
        'userstatus', 'login_as_user')
    list_filter = ('user__date_joined', 'user__last_login', 'userstatus')
    search_fields = ('user__email', 'user__username')

    def login_as_user(self, obj):
        return format_html("<a href='http://sabzicart.in/accounts/signin/{}/'>login</a>", obj.user.username)

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def last_login(self, obj):
        return obj.user.last_login

    def date_joined(self, obj):
        return obj.user.date_joined

    def user_email(self, obj):
        return obj.user.email

    def username(self, obj):
        return obj.user.username

class UserUsageAdmin(admin.ModelAdmin):
    list_display = ('username', 'quantity', 'price', 'active', 'date')
    list_filter = ('userusage__user',)

    def username(self, obj):
        return obj.userusage.user.username


class PayableAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'payable')
    list_filter = ('date', 'payable')

    # def get_queryset(self, request):
    #     qs = super(PayableAdmin, self).get_queryset(request)
    #     return qs.exclude(payable__lt=100)


admin.site.register(UserUsage, UserUsageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payable, PayableAdmin)
admin.site.register(Holidays)
admin.site.register(Reinvestment)

