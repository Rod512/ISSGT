from django.contrib import admin
from .models import HomeBlog

class AdminHomeBlog(admin.ModelAdmin):
    list_display = ('category', 'slug', 'published_date', 'image', 'is_featured')

admin.site.register(HomeBlog,AdminHomeBlog)
