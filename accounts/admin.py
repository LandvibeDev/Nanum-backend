from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import NanumUser

class NanumUserInline(admin.StackedInline):
    model = NanumUser
    can_delete = True

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (NanumUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)