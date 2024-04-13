from django.urls import path
from .views import SignUpView, LogInView, LogOutView, EmailVerificationView

urlpatterns = [
    path('sign_up', SignUpView.as_view(), name='sign-up'),
    path('log_in', LogInView.as_view(), name='log-in'),
    path('log_out', LogOutView.as_view(), name='log-out'),
    path('email_verification/<token>/<uidb64>', EmailVerificationView.as_view(), name="email verification")
]