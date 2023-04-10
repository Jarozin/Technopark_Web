from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Answer)
admin.site.register(models.Tag)
admin.site.register(models.Like)
admin.site.register(models.AskmeUser)
admin.site.register(models.Question)
admin.site.register(models.CommonContent)
