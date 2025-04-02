from django.contrib import admin
from .models import Comment

class AdminComment(admin.ModelAdmin):
    list_display = ('user', 'comment', 'blog', 'created_at')

admin.site.register(Comment, AdminComment)
