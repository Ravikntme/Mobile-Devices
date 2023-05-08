from django.contrib import admin
from .models import Mobile
# Register your models here.

@admin.register(Mobile)
class Mobileadmin(admin.ModelAdmin):
    list_display = ['brand','model','colour','price']