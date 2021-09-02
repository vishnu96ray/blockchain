from datetime import timedelta, datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import *
from import_export.admin import ImportExportModelAdmin


class UserProfileAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'applicant', 'sodowo','gender','dob','age','pan','joining_amt','district','city','state','pincode','address',
        'sponsor_name','sponsor_mobile', 'user_referral', 'referral_code','receipt_pic', 'referred_by', 'level',
        'user_email', 'username', 'mobile', 'first_name', 'last_name', 'last_login', 'date_joined', 'address',
        'userstatus', 'login_as_user', 'account_no', 'ifsc_code')
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


class PayableAdmin(ImportExportModelAdmin):
    actions = ['activate_payable']
    list_display = ('user', 'name', 'joining_date', 'date', 'last_date', 'days', 'payable', 'is_activated')
    list_filter = ('date', 'payable')

    @admin.action(description='Activate Payable')
    def activate_payable(self, request, queryset):
        queryset.update(is_activated=True)

    def get_queryset(self, request):
        qs = super(PayableAdmin, self).get_queryset(request)
        return qs.exclude(payable__lt=100)

    def name(self, obj):
        return obj.user.user

    def joining_date(self, obj):
        rein = obj.user.reinvestment_set.order_by('-date').first()
        if rein is None:
            return obj.user.user.date_joined
        else:
            return rein.date

    def last_date(self, obj):
        return obj.user.user.date_joined + timedelta(days=270)

    def days(self, obj):
        date = obj.user.user.date_joined + timedelta(days=270)
        return (date.date() - datetime.now().date()).days


admin.site.register(UserUsage, UserUsageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payable, PayableAdmin)
admin.site.register(Holidays)
admin.site.register(Reinvestment)

