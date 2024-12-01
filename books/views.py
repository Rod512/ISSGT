from django.shortcuts import render
from .models import Books
from django.core.paginator import Paginator

def books(request):
    book_list = Books.objects.all()
    paginator = Paginator(book_list, 5)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    book_page_obj = paginator.get_page(page_number)
    context = {
        # 'book_list': book_list
        'book_page_obj': book_page_obj
    }
    return render(request, 'books/books.html', context)
