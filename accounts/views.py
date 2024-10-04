from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import Rule, CustomUser
from borrows.models import Borrow
from reserves.models import Reserve
from datetime import date, timedelta
from books.models import Book
from django.db.models import Q
from django.db.models import Sum

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


def update_reserve_status(reserve_period):
    # Calculate the date 3 days ago from today
    three_days_ago = date.today() - timedelta(days=reserve_period)
    # Update all reserves where reserve_date is more than 3 days ago and status is 'active'
    Reserve.objects.filter(
        reserve_date__lt=three_days_ago,
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
    non_active_reserves = Reserve.objects.filter(
        Q(reserve_status='fulfilled') | Q(reserve_status='expired'))
    for reserve in non_active_reserves:
        selected_book = reserve.book
        if selected_book.book_status == 'Reserved':
            selected_book.book_status = 'Available'
            selected_book.save()
    active_reserves = Reserve.objects.filter(reserve_status='active')
    for reserve in active_reserves:
        selected_book = reserve.book
        selected_book.book_status = 'Reserved'
        selected_book.save()


def update_overdue_days():
    returned_books = Borrow.objects.filter(return_date__isnull=False)
    for returned_book in returned_books:
        day_delta = returned_book.return_date - returned_book.due_date
        returned_book.overdue_days = day_delta.days
        returned_book.save()


def update_book_fine(fine_per_day):
    Borrow.objects.filter(fine_paid=True).update(book_fine=0)
    unpaid_borrows = Borrow.objects.filter(
        Q(fine_paid=False) & Q(return_date__isnull=False)
    )
    for unpaid_borrow in unpaid_borrows:
        unpaid_borrow.book_fine = unpaid_borrow.overdue_days * fine_per_day
        unpaid_borrow.save()


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
        Q(overdue_days__gt=0) &
        Q(return_date__isnull=False) &
        Q(fine_paid=False) & Q(user=user)
    )
    total_fine = overdue_unpaid_borrows.aggregate(
        Sum('book_fine'))['book_fine__sum'] or 0

    reserved_items = Reserve.objects.filter(reserve_status='active', user=user)

    context = {'unreturned_borrows': unreturned_borrows_per_user,
               'overdue_unpaid_borrows': overdue_unpaid_borrows,
               'total_fine': total_fine,
               'reserved_items': reserved_items}
    return render(request, 'accounts/dashboard.html', context)


def forgotpass(request):
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
            return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('changepass')
    else:
        return render(request, 'accounts/changepass.html')
