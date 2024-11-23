from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages
from .models import Account

def login(request): 
    return render(request, 'account/login.html')

from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from .models import Account

def login(request): 
    return render(request, 'account/login.html')

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
            user.save()  # Save the user object with the phone number
            
            # Success message
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'account/registration.html', {'form': form})

