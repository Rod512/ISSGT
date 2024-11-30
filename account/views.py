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
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')
