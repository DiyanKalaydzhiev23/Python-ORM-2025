from django.contrib import admin
from main_app.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ...