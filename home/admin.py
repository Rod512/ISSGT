from django.contrib import admin
from .models import HomeBlog


class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date')

admin.site.register(HomeBlog, HomeAdmin)

