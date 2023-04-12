from functools import wraps
from django.shortcuts import redirect
from .models import User
def login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            return redirect('login')
        user = request.session.get('email')
        users = User.objects.get(email=user)
        if users.register_as != 2:
            return redirect('coordinator_dashboard')
        elif users.register_as != 1:
            return redirect('player_dashboard')
        else:
            return function(request, *args, **kwargs)
    return wrapper
