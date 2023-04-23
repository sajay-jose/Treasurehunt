from django.contrib import admin
from .models import User, Game, Level, Game_login

# Register your models here.
admin.site.register(User)
admin.site.register(Game)
admin.site.register(Level)
admin.site.register(Game_login)