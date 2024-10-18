from django.shortcuts import render
from .models import HomeBlog

def home(request):
    blogs = HomeBlog.objects.all().order_by('published_date')

    context = {
        'blogs': blogs
    }
    return render(request, 'home/index.html', context)
