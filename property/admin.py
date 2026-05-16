from django.contrib import admin
from .models import Flat

class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'address', 'owner')

# ВАЖНО: Передай FlatAdmin вторым аргументом
admin.site.register(Flat, FlatAdmin)