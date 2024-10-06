from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('forgotpass', views.forgotpass, name='forgotpass'),
    path('changepass', views.changepass, name='changepass'),
    path('create-checkout-session', views.create_checkout_session,
         name='create_checkout_session'),
    path('payment-success', views.payment_success,
         name='payment_success'),
    path('payment-failure', views.payment_failure,
         name='payment_failure'),
]
