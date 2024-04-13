from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import BaseUser
import smtplib, ssl
from .forms import SignUpForm, LoginForm
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from jobposting.models import Employer

# Create your views here.
class SignUpView(View):
    form_type = SignUpForm
    template_name = 'user_management/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_type(request.GET)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_type(request.POST)

        if form.is_valid():
            user = form.save()
            account_type = form.cleaned_data.get('account_type')

            if account_type == '2':
                # Create an Employer object
                employer = Employer.objects.create(user=user, email=user.email)
                # Assuming you have a ForeignKey relation to Job model, handle accordingly

            # send email
            port = 587  # For starttls
            smtp_server = "smtp.gmail.com"
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            to = user.username
            fromEmail = "privacyjobboard@gmail.com" 
            password = "euoq nrjx lmdc moks"
            email_message = MIMEMultipart('alternative')
            email_message["Subject"] = "Email Verification Privacy Job Board"
            email_message["From"] = fromEmail
            email_message["To"] = to

            html = """\
            <html>
            <body>
                <p>Please Verify Your Account
                <a href="http://127.0.0.1:8000/user/email_verification/{}/{}">Verify your Account</a> 
                </p>
            </body>
            </html>
            """.format(token, uid)

            email_message.attach(MIMEText(html, "html"))
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(fromEmail, password)
                server.sendmail(fromEmail, to, email_message.as_string())

            return redirect(to='/')
        return render(request, self.template_name, {'form': form})
    
class LogInView(LoginView):
    # TODO prevent login if user is not verified
    form_class = LoginForm
    template_name = 'user_management/login.html'

class LogOutView(LogoutView):
    template_name = 'user_management/logout.html'

class EmailVerificationView(View):
    template_name = 'user_management/email_verification.html'

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = BaseUser.objects.get(pk=uid)
        token = kwargs['token']
        if user is not None and default_token_generator.check_token(user, token):
            user.verified = True
            user.save()
        return render(request, self.template_name)