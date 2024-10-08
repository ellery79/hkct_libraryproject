# Standard Library Imports
from datetime import date, timedelta
import json
import random
import string

# Third-Party Imports
from decouple import config
import stripe
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.db.models import Q, Sum, F
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Local App Imports
from .models import Rule, CustomUser
from borrows.models import Borrow
from reserves.models import Reserve
from books.models import Book

# Create your views here.

stripe.api_key = config('STRIPE_SECRET_KEY')
stripe_publishable_key = config('STRIPE_PUBLISHABLE_KEY')


def login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!')
        return render(request, 'pages/index.html')

    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user:
        auth.login(request, user)
        messages.success(request, "You are now logged in")
        return redirect('dashboard')

    messages.error(request, 'Invalid credentials or password')
    return redirect('login')


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

    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    required_fields = ['first_name', 'last_name', 'username',
                       'email', 'password', 'password2', 'card_id', 'user_phone']
    data = {field: request.POST.get(field) for field in required_fields}

    if data['password'] != data['password2']:
        messages.error(request, 'Passwords do not match')
        return redirect('register')

    if CustomUser.objects.filter(username=data['username']).exists():
        messages.error(request, 'Username already exists')
        return redirect('register')

    if CustomUser.objects.filter(email=data['email']).exists():
        messages.error(request, 'Email already exists')
        return redirect('register')

    try:
        default_rule = Rule.objects.get(rule_name="default")
        user = CustomUser.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            card_id=data['card_id'],
            user_phone=data['user_phone'],
            rule=default_rule
        )
        messages.success(request, "You are now registered and can log in")
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"An error occurred during registration: {str(e)}")
        return redirect('register')


def update_reserve_status(reserve_period):
    threshold_date = timezone.now().date() - timezone.timedelta(days=reserve_period)
    Reserve.objects.filter(
        reserve_date__lt=threshold_date,
        reserve_status='active',
    ).update(reserve_status='expired')


def update_book_borrow_status():
    # Filter Borrow objects where return_date is null
    borrows_with_no_return_date = Borrow.objects.filter(
        return_date__isnull=True)

    # Filter Borrow objects where return_date is not null
    borrows_with_return_date = Borrow.objects.filter(return_date__isnull=False)

    # Find Borrow objects that are in borrows_with_return_date but not in borrows_with_no_return_date
    borrows_with_return_date_only = borrows_with_return_date.exclude(
        book__in=borrows_with_no_return_date.values('book'))
    for borrow in borrows_with_no_return_date:
        selected_book = borrow.book
        selected_book.book_status = 'Borrowed'
        selected_book.save()
    for borrow in borrows_with_return_date_only:
        selected_book = borrow.book
        if selected_book.book_status == 'Borrowed':
            selected_book.book_status = 'Available'
            selected_book.save()


def update_book_reserve_status():
    # Update books from 'Reserved' to 'Available'
    Book.objects.filter(
        reserve__reserve_status__in=['fulfilled', 'expired'],
        book_status='Reserved'
    ).update(book_status='Available')

    # Update books to 'Reserved'
    Book.objects.filter(
        reserve__reserve_status='active'
    ).update(book_status='Reserved')


def update_overdue_days():
    returned_books = Borrow.objects.filter(return_date__isnull=False)
    for returned_book in returned_books:
        day_delta = returned_book.return_date - returned_book.due_date
        returned_book.overdue_days = day_delta.days
        returned_book.save()


def update_book_fine(fine_per_day):
    # Reset fines for paid borrows
    Borrow.objects.filter(fine_paid=True).update(book_fine=0)

    # Calculate fines for unpaid borrows
    Borrow.objects.filter(
        fine_paid=False,
        return_date__isnull=False
    ).update(book_fine=F('overdue_days') * fine_per_day)

def get_user_data(user):
    return {
        'unreturned_borrows': Borrow.objects.filter(user=user, return_date__isnull=True),
        'overdue_unpaid_borrows': Borrow.objects.filter(
            overdue_days__gt=0,
            return_date__isnull=False,
            fine_paid=False,
            user=user
        ),
        'reserved_items': Reserve.objects.filter(reserve_status='active', user=user),
    }

def dashboard(request):
    if not request.user.is_authenticated:
        messages.info(
            request, 'Please login before you can see dashboard')
        return render(request, 'accounts/login.html')
    user = request.user
    reserve_period = user.rule.reserve_period
    fine_per_day = user.rule.fine_per_day
    update_reserve_status(reserve_period)
    update_book_reserve_status()
    update_book_borrow_status()
    update_overdue_days()
    update_book_fine(fine_per_day)
    unreturned_borrows_per_user = Borrow.objects.filter(
        user=user, return_date__isnull=True)
    overdue_unpaid_borrows = Borrow.objects.filter(
        overdue_days__gt=0,
        return_date__isnull=False,
        fine_paid=False,
        user=user,
    )
    total_fine = overdue_unpaid_borrows.aggregate(
        Sum('book_fine'))['book_fine__sum'] or 0
    reserved_items = Reserve.objects.filter(reserve_status='active', user=user)
    context = {'unreturned_borrows': unreturned_borrows_per_user,
               'overdue_unpaid_borrows': overdue_unpaid_borrows,
               'total_fine': total_fine,
               'reserved_items': reserved_items,
               'stripe_publishable_key': stripe_publishable_key,
               }
    return render(request, 'accounts/dashboard.html', context)


def email_new_password(myEmail, domain, password, toEmail):
    send_mail(
        "New password for ABC Library",  # subject
        f"You're receiving this email because you requested a password reset for your user account at {domain}. \n Your new password is {password} \n Please login here: http://{domain}/accounts/login",
        myEmail,  # from email
        [toEmail],
        fail_silently=False,
    )


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def forgotpass(request):
    match request:
        case _ if request.user.is_authenticated:
            messages.info(
                request, 'You have logged in and can change your password here')
            return render(request, 'accounts/changepass.html')

        case _ if request.method == 'POST':
            user_email = request.POST.get('email')
            match CustomUser.objects.filter(email=user_email).first():
                case None:
                    messages.error(
                        request, "Email is invalid. Please enter a correct email.")
                case selected_user:
                    myEmail = config('MY_EMAIL')
                    domain = request.get_host()
                    new_password = generate_password(length=8)
                    email_new_password(
                        myEmail, domain, new_password, user_email)
                    selected_user.set_password(new_password)
                    selected_user.save()
                    messages.success(
                        request, "Email sent. If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder.")
            return redirect('forgotpass')

        case _:
            return render(request, 'accounts/forgotpass.html')


def changepass(request):
    if not request.user.is_authenticated:
        messages.info(
            request, 'Please login before you can change password!')
        return render(request, 'accounts/login.html')
    if request.method == 'POST':
        new_password = request.POST['password']
        con_password = request.POST['password2']
        if new_password == con_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(
                request, 'You are success change password and login with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('changepass')
    else:
        return render(request, 'accounts/changepass.html')


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            domain = request.get_host()
            data = json.loads(request.body)
            customer_email = request.user.email
            total_amount = int(data.get('total_amount')
                               * 100)  # Convert to cents
            session = stripe.checkout.Session.create(
                customer_email=customer_email,
                line_items=[{
                    'price_data': {
                        'currency': 'hkd',
                        'product_data': {
                            'name': 'Overdue Charges',
                        },
                        'unit_amount': total_amount,
                    },
                    'quantity': 1,
                }],
                automatic_tax={"enabled": False},
                mode='payment',
                success_url=f'http://{domain}/accounts/payment-success',
                cancel_url=f'http://{domain}/accounts/payment-failure',
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def payment_success(request):
    user = request.user
    Borrow.objects.filter(
        overdue_days__gt=0,
        return_date__isnull=False,
        fine_paid=False,
        user=user,
    ).update(fine_paid=True)
    messages.success(
        request, 'Payment success!')
    return redirect('dashboard')


def payment_failure(request):
    messages.error(
        request, 'Payment failed!')
    return redirect('dashboard')
