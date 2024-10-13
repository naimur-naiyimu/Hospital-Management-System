from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.user_type in allowed_roles  or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                # Return JavaScript to show a pop-up alert
                message = "You are not authorized to view this page. Thank you."
                return HttpResponse(loader.get_template('popup_alert.html').render({"script": f"alert('{message}');"}, request))

        return wrapper_func
    return decorator
