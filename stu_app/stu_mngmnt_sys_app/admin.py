from django.contrib import admin
from stu_mngmnt_sys_app.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
