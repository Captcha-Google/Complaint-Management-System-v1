from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def restricted_path(view_func):
    def wrapper_func(request,*args, **kwargs): 
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request,*args, **kwargs)
        else:
            return redirect('/dashboard/')
    return wrapper_func