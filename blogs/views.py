from django.core.paginator import Paginator
from django.shortcuts import render
from home.models import HomeBlog
from django.shortcuts import render, get_object_or_404


def blog_list(request):
    # Fetch all blogs for the blog page
    blogs = HomeBlog.objects.all().order_by('-published_date')
    paginator = Paginator(blogs, 5)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'blogs/blogs.html', context)

def single_blog(request, slug):
    blog = get_object_or_404(HomeBlog, slug=slug)  # Get the specific blog post by its slug
    return render(request, 'blogs/single_blog.html', {'blog': blog})