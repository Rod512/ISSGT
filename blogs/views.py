from django.shortcuts import render

def blogs(request):
    return render(request, 'blogs/blogs.html')
