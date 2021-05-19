from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.models import UserProfile


def unapproved_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user).first()
            if profile.is_approved:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Sorry.. Your profile has not been approved yet. Please wait for a few days while our admin reviews your profile')
        return redirect('/')
    return wrapper_func
