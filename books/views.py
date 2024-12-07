from django.shortcuts import render
from .models import Books
from django.core.paginator import Paginator
from django.db.models import Q


def books(request):
    keyword = request.GET.get('keyword', '').strip()
    
    
    if keyword:
        book_list = Books.objects.filter(
            Q(book_name__icontains=keyword) |
            Q(book_author__icontains=keyword)
        ).order_by('-uploaded_at')
    else:
        book_list = Books.objects.all().order_by('-uploaded_at')
    
    
    paginator = Paginator(book_list, 5)  
    page_number = request.GET.get('page')
    book_page_obj = paginator.get_page(page_number)

    context = {
        'book_page_obj': book_page_obj,
        'keyword': keyword, 
    }
    return render(request, 'books/books.html', context)
