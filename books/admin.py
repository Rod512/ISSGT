from django.contrib import admin
from .models import Books

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'book_author',  'uploaded_at')

admin.site.register(Books, BookAdmin)
