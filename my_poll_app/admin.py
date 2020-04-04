from django.contrib import admin

from .models import Poll, User

admin.site.register(Poll)
admin.site.register(User)
