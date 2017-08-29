from django.http import HttpResponseBadRequest
from authentication.models import Utilisateur



def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap



def is_businessuser(f):
    def wrap(request, *args, **kwargs):
        if not Utilisateur.objects.filter(user=request.user).exists():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap    