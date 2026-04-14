from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm
from .models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.role == 'staff':
                return redirect('appointment_dashboard')
            else:
                return redirect('service_dashboard')
        except:
            return redirect('service_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    
                    # Xử lý ghi nhớ đăng nhập
                    if not remember_me:
                        request.session.set_expiry(0)
                    
                    # Redirect dựa vào role
                    try:
                        profile = user.profile
                        if profile.role == 'staff':
                            return redirect('appointment_dashboard')
                        else:
                            return redirect('service_dashboard')
                    except:
                        return redirect('service_dashboard')
                else:
                    messages.error(request, 'Email hoặc mật khẩu không chính xác!')
            except User.DoesNotExist:
                messages.error(request, 'Email không tồn tại trong hệ thống!')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.role == 'staff':
                return redirect('appointment_dashboard')
            else:
                return redirect('service_dashboard')
        except:
            return redirect('service_dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('login')
        else:
            # Hiển thị lỗi validation
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('login')


@login_required(login_url='login')
def profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, role='customer')
    
    return render(request, 'auth/profile.html', {'profile': profile})

