from django.shortcuts import render

from .models import HomeBlog
from django.utils.timezone import now
from django.db.models import Q
# from .forms import SearchForm
from django.contrib import messages


def home(request):
    featured_blogs = HomeBlog.objects.filter(is_featured=True).order_by('-published_date')
    if not featured_blogs.exists():
        featured_blogs = HomeBlog.objects.all().order_by('-published_date')  

    # টেমপ্লেটের জন্য `blogs` কনটেক্সট যোগ করো
    blogs = HomeBlog.objects.all().order_by('-published_date')

    context = {
        'featured_blogs': featured_blogs,
        'blogs': blogs,
        'version': now().timestamp(),
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
    else:
        blogs = HomeBlog.objects.all().order_by('-published_date')
        print(f"Found {blogs.count()} blogs")

    context = {
        'blogs': blogs,
    }

    return render(request, 'home/index.html', context)






    