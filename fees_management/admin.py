from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . models import *


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'


class UserAdmin(BaseUserAdmin):
    inlines = [StudentInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Institute)
admin.site.register(Branch)
admin.site.register(Course)
admin.site.register(Transaction)
