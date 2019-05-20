from django.contrib import admin
from .models import PollUser,Section, EventDay
# Register your models here.

admin.site.register(PollUser)
admin.site.register(Section)
admin.site.register(EventDay)
