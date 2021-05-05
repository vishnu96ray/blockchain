from functools import wraps
import json
# from payment.models import AppAccess
# from django.utils.decorators import available_attrs
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url


def login_required_ajax(view_func):
    # @wraps(view_func, assigned=available_attrs(view_func))
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            if request.is_ajax():  # or request.method == "POST":
                return HttpResponse(json.dumps(5), content_type="application/json")
            else:
                # path = request.build_absolute_uri()
                path = request.get_full_path()
                resolved_login_url = resolve_url("/")
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(path, resolved_login_url)

    return _wrapped_view


# def access_required(access_permissions=None):
#     def _method_wrapper(view_func):
#         def _arguments_wrapper(request, *args, **kwargs):
#             applist_id = AppAccess.objects.filter(app_list__name=access_permissions,payment_plan=request.user.userdetail.myplan)
#             if not applist_id:
#                 return HttpResponseRedirect("/insite/payment/purchase-credit/")
#             else:
#                 return view_func(request, *args, **kwargs)
#         return _arguments_wrapper
#     return _method_wrapper
