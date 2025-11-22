from django.contrib import admin
from .models import Library, Author, Genre, Availability, Book


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'total_books', 'contact')
    search_fields = ('name', 'area')
    list_filter = ('area',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ('status',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'library', 'availability')
    search_fields = ('title', 'author__name', 'genre__name')
    list_filter = ('genre', 'availability', 'library')
