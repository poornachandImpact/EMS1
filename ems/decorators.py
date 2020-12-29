from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

# Dinamic roles decorator
def role_required(allowed_roles=[]):
    def decorator(func):    #func r  view_func
        def wraps(request,*args,**kwargs):
            if request.role in allowed_roles:
                return func(request,*args,**kwargs)
            else:
                return HttpResponseRedirect(reverse('employee_list'))
        return  wraps
    return decorator

# static Role Decorator

def admin_only(func):
    def wraps(request,*args,**kwargs):
            if request.role == "Admin":
                return func(request,*args,**kwargs)
            else:
                return HttpResponseRedirect(reverse('employee_list'))
    return  wraps
