from django.contrib import admin

from .models import *


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'idd', 'ccd', 'iso_code', 'active', 'user', 'added_date', 'modified_date')
    list_filter = ('active',)
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'added_date', 'email', 'skypeid', 'country_detail', 'mobile', 'message', 'status')
    list_editable = ('status',)
    # list_filter = ('page',)
    def country_detail(self, obj):
        if obj.country:
            return obj.country.name + "-idd-%s, ccd-+%s" % (obj.country.idd, obj.country.ccd)
        else:
            return ''


class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('active',)

admin.site.register(Country, CountryAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(Tag, TagAdmin)
