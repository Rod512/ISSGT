from django.core.paginator import Paginator
from django.shortcuts import render
from home.models import HomeBlog
from .models import Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def blog_list(request):
    # Fetch all blogs for the blog page
    blogs = HomeBlog.objects.all().order_by('-published_date')
    paginator = Paginator(blogs, 4)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'blogs/blogs.html', context)

def single_blog(request, slug):
    blog = get_object_or_404(HomeBlog, slug=slug)
    comment = Comment.objects.filter(blog=blog).order_by('-created_at')
    
    context ={
        'blog': blog,
        'comment' : comment
    }  
    return render(request, 'blogs/single_blog.html', context)

@login_required
def add_comment(request, slug):
    blog = get_object_or_404(HomeBlog, slug=slug)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                blog=blog,
                user=request.user,
                comment=content,
            )
            comment.save()
            return redirect('single_blog', slug=blog.slug)
    return redirect('single_blog', slug=blog.slug)