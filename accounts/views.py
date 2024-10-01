from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import Rule, CustomUser
from borrows.models import Borrow
from reserves.models import Reserve

# Create your views here.


def login(request):

    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!')
        return render(request, 'pages/index.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        messages.info(
            request, 'You are already logged in! Please log out before register.')
        return render(request, 'pages/index.html')
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        card_id = request.POST['card_id']
        user_phone = request.POST['user_phone']
        default_rule = Rule.objects.get(rule_name="default")

        if password == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                else:
                    user = CustomUser.objects.create_user(username=username,
                                                          password=password,
                                                          email=email,
                                                          first_name=first_name,
                                                          last_name=last_name,
                                                          card_id=card_id,
                                                          user_phone=user_phone,
                                                          rule=default_rule)
                    user.save()
                    messages.success(
                        request, "You are now registered and can log in")
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')




def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotpass(request):
    return render(request, 'accounts/forgotpass.html')


def changepass(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        selected_user = CustomUser.objects.filter(username=username)
        selected_user.set_password(password)
        selected_user.save()
        return render(request, 'accounts/changepass.html')
    return render(request, 'accounts/changepass.html')
