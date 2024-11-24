from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from .models import Account
from django.contrib.auth import authenticate, login
from urllib.parse import urlparse, parse_qs


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
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'account/registration.html', {'form': form})




def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate using the default authentication system
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in if authentication is successful
            login(request, user)
            messages.info(request, "You have successfully logged in.")
            url = request.META.get("HTTP_REFERER")
            try:
                query = urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except Exception:
                return redirect("dashboard")  # Replace with your dashboard or homepage URL
        else:
            messages.warning(request, "Invalid login credentials")
            return redirect("login")
    else:
        return render(request, "account/login.html")


