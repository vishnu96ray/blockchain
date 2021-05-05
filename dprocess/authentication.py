from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from accounts.models import UserProfile

class APIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        apikey = request.GET.get('apikey')
        if not apikey:
            return None
        try:
            userprofile = UserProfile.objects.get(key=apikey)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (userprofile.user, None)