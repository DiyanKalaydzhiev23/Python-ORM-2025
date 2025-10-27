from django.contrib import admin
from main_app.models import Laptop


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    ...
