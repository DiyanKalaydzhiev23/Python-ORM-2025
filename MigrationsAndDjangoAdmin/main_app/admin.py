from django.contrib import admin
from unfold.admin import ModelAdmin
from main_app.models import EventRegistration, Movie, Student, Supplier, Course


@admin.register(EventRegistration)
class EventRegistrationAdmin(ModelAdmin):
    list_display = ['event_name', 'participant_name', 'registration_date']
    list_filter = ['event_name', 'registration_date']
    search_fields = ['event_name', 'participant_name']


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = ['title', 'director', 'release_year', 'genre']
    list_filter = ['release_year', 'genre']
    search_fields = ['title', 'director']


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'age', 'grade']
    list_filter = ['age', 'grade', 'date_of_birth']
    search_fields = ['first_name']

    fieldsets = (
        ("Personal Information", {
            'fields': ('first_name', 'last_name', 'age', 'date_of_birth')
        }),
        ("Academic Information", {
            'fields': ('grade',)
        })
    )

@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ['name', 'email', 'phone']
    list_filter = ['name', 'phone']
    search_fields = ['email', 'contact_person', 'phone']
    list_per_page = 20

    fieldsets = (
        ('Information', {
            'fields': ('name', 'contact_person', 'email', 'address'),
        }),
    )


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ['title', 'lecturer', 'price', 'start_date']
    list_filter = ['is_published', 'lecturer']
    search_fields = ['title', 'lecturer']
    readonly_fields = ['start_date']

    fieldsets = [
        ('Course Information', {
            'fields': [
                'title',
                'lecturer',
                'price',
                'start_date',
                'is_published',
            ],
        }),
        ('Description', {
            'fields': [
                'description',
            ],
        })
    ]