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
from .decoretor import unauthenticated_required
from home.models import HomeBlog,Category
from home.forms import Homeblogform, CategoryForm
from books.models import Books
from books.forms import BookForm


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from contact.models import Contact






@unauthenticated_required
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
@user_passes_test(is_admin, login_url='home')
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
@user_passes_test(is_admin, login_url='home')
def delete_post(request, slug):
    blog = get_object_or_404(HomeBlog, slug=slug)

    if request.method == 'POST':  
        blog.delete()
        messages.success(request, "The blog post has been deleted successfully.")
        return redirect('dashboard')  

    return render(request, 'account/delete_post.html', {'blog': blog})

@login_required
@user_passes_test(is_admin, login_url='home')
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
@user_passes_test(is_admin, login_url='home')
def delete_books(request, book_id):
    books = get_object_or_404(Books, id=book_id)
    if request.method == 'POST':
        books.delete()
        messages.success(request, "The book has been deleted successfully.")
        return redirect('dashboard')
    return render(request, 'account/delete_books.html', {'books': books})



def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('account/reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_mail = email
            send_mail = EmailMessage(mail_subject, message, to=[to_mail])
            send_mail.send()
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
    return render(request,'account/forgotPassword.html')


def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'invalid link')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'password does not match')
            return redirect('resetpassword')
    else:
        return render(request,'account/resetPassword.html')
    

from django.contrib.auth import logout

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                logout(request)
                messages.success(request, 'Password updated successfully. Please login again.')
                return redirect('login')
            else:
                messages.error(request, 'Current password is not correct')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('change_password')
    return render(request, 'account/change_password.html')


@login_required
@user_passes_test(is_admin, login_url='home')
def contact_messages(request):
    messages_list = Contact.objects.all().order_by('-created_at') 
    return render(request, 'account/contact_messages.html', {'messages_list': messages_list})

@login_required
@user_passes_test(is_admin, login_url='home')
def read_message(request, message_id):
    message_obj = get_object_or_404(Contact, id=message_id)
    if not message_obj.is_read:
        message_obj.is_read = True
        message_obj.save()
    return render(request, 'account/read_message.html', {'message': message_obj})

@login_required
@user_passes_test(is_admin, login_url='home')
def delete_message(request, message_id):
    message_obj = get_object_or_404(Contact, id=message_id)
    message_obj.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('contact_messages')