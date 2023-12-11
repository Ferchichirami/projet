from django.contrib import admin
from .models import *
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Material)
admin.site.register(ReadingState)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Grade)
admin.site.register(InteractionHistory)
# Register your models here.
