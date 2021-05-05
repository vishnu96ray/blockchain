from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

Query_STATUS = ((1, 'Submited'), (2, 'Replied'), (3, 'In Queue'), (4, 'Closed'))


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(ModelBase):
    name = models.CharField(_('Country Name'), max_length=100)
    idd = models.CharField(_("International Dialing Digit "), max_length=5, blank=True, null=True)
    ccd = models.IntegerField(_("Country Calling Code "), default=0)
    iso_code = models.CharField(_('ISO Code'), max_length=100, blank=True)

    def __str__(self):
        return self.name


class BusinessType(ModelBase):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class State(ModelBase):
    name = models.CharField(_('State Name'), max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class City(ModelBase):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('City Name'), max_length=100)

    def __str__(self):
        return self.name


class Tag(ModelBase):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    skypeid = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.IntegerField(_("Status"), choices=Query_STATUS, default=1)
