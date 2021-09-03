from django.contrib import admin
from .models import PollUser,Section, EventDay, USR
# Register your models here.

admin.site.register(PollUser)
admin.site.register(Section)
admin.site.register(EventDay)
admin.site.register(USR)
