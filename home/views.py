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

    # Default: No blogs
    blogs = HomeBlog.objects.none()

    if keyword:
        # Exact match first
        exact_match = HomeBlog.objects.filter(
            Q(blog_name__iexact=keyword) |  # Exact match with blog name
            Q(category__name__iexact=keyword) |  # Exact match with category name
            Q(author__username__iexact=keyword)  # Exact match with author username
        )
        
        # Partial match (icontains)
        partial_match = HomeBlog.objects.filter(
            Q(blog_name__icontains=keyword) |
            Q(category__name__icontains=keyword) |
            Q(content__icontains=keyword) |
            Q(author__username__icontains=keyword)
        ).exclude(id__in=exact_match)  # Avoid duplicates
        
        # Combine results
        blogs = exact_match | partial_match  # Combine exact and partial matches
        blogs = blogs.order_by('-published_date')  # Sort by published date

        # Message for the user
        if blogs.exists():
            messages.info(request, f"Search results for '{keyword}': {blogs.count()} blogs found.")
        else:
            messages.warning(request, f"No blogs found for '{keyword}'.")
    else:
        messages.info(request, "Please enter a keyword to search.")

    # Pass categories and other home context
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
        'blogs': blogs,  # Pass filtered blogs
        'search_keyword': keyword,  # Pass search keyword to the template
        'version': now().timestamp(),
    }

    return render(request, 'home/index.html', context)











    