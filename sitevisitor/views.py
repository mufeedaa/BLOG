from django.shortcuts import render, redirect
from adminpanel.models import  Blog,  Profile, User
from userpanel.forms import BlogForm , RegistrationForm, ProfileForm, LoginForm, SiteResetPasswordForm, ForgotPasswordForm, OtpForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    blogs = Blog.objects.filter(status = 'PUBLISH').order_by('-updated_at').filter(author__is_active = True)
    return render(request, 'sitevisitor/home.html', {'blogs': blogs})    

def logged_user_data(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    return logged_user, profile


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('user_home')
            else:
                messages.error(request, 'Invalid Usename or Password!!')
                return redirect('site_login')    

    else:
        form = LoginForm() 
    return render(request, 'sitevisitor/login.html', {'form': form})       
    

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        pro_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and pro_form.is_valid():
            user = form.save()
            profile = pro_form.save(commit = False)
            profile.user = user
            profile.save()
            
            messages.success(request,'Successfully registered')
            return redirect('site_login')
    else:
        form = RegistrationForm()
        pro_form = ProfileForm
       
    return render(request, 'sitevisitor/registration.html', {'form': form, 'pro_form': pro_form})  

            


def forgotpassword(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email = email).exists():
                messages.success(request, 'Instructions to reset your password.')
                return redirect('site_otp')
            else:
                messages.error(request,'This email id does not exist!!')
                return redirect('site_forgotpassword')

    else:
        form = ForgotPasswordForm()                
    return render(request, 'sitevisitor/forgot_password.html', {'form':form})    

def resetpassword(request):
    if request.method == 'POST':
        form = SiteResetPasswordForm( request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password3 = form.cleaned_data.get('password3')
            password4 = form.cleaned_data.get('password4')

            if password3 != password4:
                form.add_error('password4', 'Passwords do not match.')
            else:
                user = User.objects.filter(username = username).first()
                if user:
                    user.set_password(password3)

                    user.save()
                    messages.success(request,'Your password has been updated successfully.')
                    return redirect('site_login')
                else:
                    form.add_error('username', 'User does not exist.')
            
        else:
            messages.error(request, 'Please correct the errors.')
    else:        
        form = SiteResetPasswordForm()   
    return render(request, 'sitevisitor/reset_password.html', {'form':form})    

def otp(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'OTP verified successfully..')
            return redirect('site_resetpassword')
        else:
            messages.error(request, 'Invalid OTP. please try again..')
            return redirect('site_otp')
    else:
        form = OtpForm()            

    return render(request, 'sitevisitor/otp.html', {'form':form})    


def error_page(request):
    return render(request,'sitevisitor/404.html')