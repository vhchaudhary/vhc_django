from django.contrib import admin

from . models import *

admin.site.register(Institute)
admin.site.register(Branch)
admin.site.register(Course)
admin.site.register(Transaction)


