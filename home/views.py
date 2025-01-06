from django.shortcuts import render

from .models import HomeBlog, Category
from django.utils.timezone import now
from django.db.models import Q
from django.contrib import messages


def home(request):
    featured_blogs = HomeBlog.objects.filter(is_featured=True).order_by('-published_date')
    if not featured_blogs.exists():
        featured_blogs = HomeBlog.objects.all().order_by('-published_date')  
    blogs = HomeBlog.objects.all().order_by('-published_date')
    categories = Category.objects.all()

    blogs_by_category = {
        category.name: HomeBlog.objects.filter(category=category).order_by('-published_date')[:5]
        for category in categories if HomeBlog.objects.filter(category=category).exists()
    }



    context = {
        'featured_blogs': featured_blogs,
        'blogs_by_category': blogs_by_category,
        'version': now().timestamp(),
        'blogs' : blogs
    }
    return render(request, 'home/index.html', context)





def search(request):
    keyword = request.GET.get('keyword', '').strip()

    if keyword:
        blogs = HomeBlog.objects.filter(
            Q(category__name__icontains=keyword) |
            Q(content__icontains=keyword) |
            Q(author__username__icontains=keyword)
        ).order_by('-published_date')
        messages.info(request, f"Search results for '{keyword}': {blogs.count()} blogs found.")
    else:
        blogs = HomeBlog.objects.none()  # No keyword, no blogs

    featured_blogs = HomeBlog.objects.filter(is_featured=True).order_by('-published_date')
    if not featured_blogs.exists():
        featured_blogs = HomeBlog.objects.all().order_by('-published_date')

    categories = Category.objects.all()
    blogs_by_category = {
        category.name: HomeBlog.objects.filter(category=category).order_by('-published_date')[:5]
        for category in categories if HomeBlog.objects.filter(category=category).exists()
    }

    context = {
        'featured_blogs': featured_blogs,
        'blogs_by_category': blogs_by_category,
        'blogs': blogs,  
        'search_keyword': keyword,
        'version': now().timestamp(),
    }

    return render(request, 'home/index.html', context)









    