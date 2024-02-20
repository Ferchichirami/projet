from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from user.models import User

TokenAdmin.raw_id_fields = ['user']
admin.site.register(User)
# Register your models here.
