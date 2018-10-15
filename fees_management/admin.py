from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


class StudentAdmin(admin.ModelAdmin):
    list_display = ('enr_no', 'get_user', 'get_first_name', 'get_last_name', 'branch', 'course')
    search_fields = ['enr_no']
    list_filter = ['is_active']

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = "User Name"

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = "Last Name"

    def delete_queryset(self, request, queryset):
        for q in queryset:
            q.is_active = False
            q.save()
        return True


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_no')
    search_fields = ['name', 'email', 'contact_no']
    list_filter = ['is_active']

    def delete_queryset(self, request, queryset):
        for q in queryset:
            q.is_active = False
            q.save()
        return True


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'institute', 'email', 'contact_no')
    search_fields = ['name', 'slug', 'email', 'contact_no']
    list_filter = ['is_active']

    def delete_queryset(self, request, queryset):
        for q in queryset:
            q.is_active = False
            q.save()
        return True


class FeeAdmin(admin.ModelAdmin):
    list_display = ('fee_type', 'branch', 'amount')
    search_fields = ['fee_type', 'branch', 'amount']
    list_filter = ['is_active']

    def delete_queryset(self, request, queryset):
        for q in queryset:
            q.is_active = False
            q.save()
        return True


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'paid_amount', 'status')
    search_fields = ['uuid', 'user', 'paid_amount', 'status']


admin.site.register(Student, StudentAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Course)
admin.site.register(Transaction, TransactionAdmin)

# class StudentInline(admin.StackedInline):
#     model = Student
#     can_delete = False
#     verbose_name_plural = 'student'

#
# class UserAdmin(BaseUserAdmin):
#     inlines = [StudentInline]
