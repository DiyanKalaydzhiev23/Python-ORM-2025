from django.contrib import admin
from unfold.admin import ModelAdmin
from main_app.models import Recipe, UserProfile, Book


@admin.register(Recipe)
class RecipeAdmin(ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass