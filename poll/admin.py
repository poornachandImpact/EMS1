from django.contrib import admin

from poll.models import *
admin.site.register(Questions)
admin.site.register(Choice)
admin.site.register(Answer)
# Register your models here.
