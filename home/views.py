from django.shortcuts import render

from .models import HomeBlog
from django.utils.timezone import now

def home(request):
    # Fetch only featured blogs for home page
    featured_blogs = HomeBlog.objects.filter(is_featured=True).order_by('-published_date')[:3]
    context = {
        'featured_blogs': featured_blogs,
        'version': now().timestamp(),
    }
    return render(request, 'home/index.html', context)

