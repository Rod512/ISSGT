from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from .models import Account
from django.contrib.auth import authenticate, login, logout


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
            
            # Success message
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('registration')
    else:
        form = RegistrationForm()
    
    return render(request, 'account/registration.html', {'form': form})



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
