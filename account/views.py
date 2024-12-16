from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from .models import Account
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required,user_passes_test

from home.models import HomeBlog,Category
from home.forms import Homeblogform, CategoryForm
from books.models import Books
from books.forms import BookForm


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse







def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            username = email.split('@')[0]  # Generating username from email
            
            # Create the user object
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            
            # Save phone number
            user.phone_number = phone_number
            user.save() 

            # user activation
            current_site = get_current_site(request)
            mail_subject = "Active Your Account"
            message = render_to_string('account/account_verification_email.html',{
                'user': user,
                'domain': current_site.domain,
                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            # Success message
            messages.success(request, 'Congratulation! Your registration successfull. We have sent a verification mail on your gmail. Please verify your aoount & login.')
            return redirect('registration')
    else:
        form = RegistrationForm()
    
    return render(request, 'account/registration.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'congratulations your account is activate')
        return redirect('login')
    else:
        messages.warning(request, 'invalid activation link')
        return redirect('registration')



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin, login_url='home')
def dashboard(request):
    # blogs
    blogs = HomeBlog.objects.filter(author=request.user)
    
    # category
    categories = Category.objects.all()

    #Books
    books = Books.objects.all()
    
    # forms
    form = Homeblogform()
    categoryform = CategoryForm()
    bookform = BookForm()

    if request.method == 'POST':
        # for blog
        if 'create_blog' in request.POST:
            form = Homeblogform(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user
                blog.save()
                messages.success(request, 'Blog created successfully')
                return redirect('dashboard')

        # for category
        elif 'create_category' in request.POST:
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                categoryform.save()
                messages.success(request, 'Category created successfully')
                return redirect('dashboard')
        
        elif 'upload_pdf' in request.POST:
            bookform = BookForm(request.POST, request.FILES)
            if bookform.is_valid():
                bookform.save()
                messages.success(request, 'Book uploaded successfully')
                return redirect('dashboard')
        

    context = {
        'blogs': blogs,
        'form': form,
        'categoryform': categoryform,
        'categories': categories,
        'bookform': bookform,
        'books': books
    }
    return render(request, 'account/dashboard.html', context)


@login_required
def edit_post(request, slug):
    blog = get_object_or_404(HomeBlog, slug=slug)

    if request.method == 'POST':
        form = Homeblogform(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = Homeblogform(instance=blog)

    return render(request, 'account/edit_post.html', {'form': form, 'blog': blog})


@login_required
def delete_post(request, slug):
    blog = get_object_or_404(HomeBlog, slug=slug)

    if request.method == 'POST':  
        blog.delete()
        messages.success(request, "The blog post has been deleted successfully.")
        return redirect('dashboard')  

    return render(request, 'account/delete_post.html', {'blog': blog})

@login_required
def edit_books(request, book_id):
    books = get_object_or_404(Books, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=books )
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error updating book')
    else:
        form = BookForm(instance=books)
    return render(request, 'account/edit_books.html', {'form': form, 'books': books })


@login_required
def delete_books(request, book_id):
    books = get_object_or_404(Books, id=book_id)
    if request.method == 'POST':
        books.delete()
        messages.success(request, "The book has been deleted successfully.")
        return redirect('dashboard')
    return render(request, 'account/delete_books.html', {'books': books})