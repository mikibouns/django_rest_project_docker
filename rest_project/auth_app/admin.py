from django.contrib import admin
from .models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'address', 'fio', 'is_superuser')

admin.site.register(Users, UsersAdmin)
