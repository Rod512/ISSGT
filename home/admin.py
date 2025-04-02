from django.contrib import admin
from .models import HomeBlog,Category

class AdminHomeBlog(admin.ModelAdmin):
    list_display = ('category', 'slug', 'published_date', 'image', 'is_featured', 'blog_name')

admin.site.register(HomeBlog,AdminHomeBlog)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}