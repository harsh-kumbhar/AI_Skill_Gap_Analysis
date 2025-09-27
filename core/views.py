from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

def home_view(request):
    return render(request, 'register.html')

# Registration View
def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')


# Login View    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # redirect to dashboard after login
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')


# Logout View
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')   # Redirects to login if not authenticated
def dashboard(request):
    return render(request, 'dashboard.html')



@login_required(login_url='login')
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.address = request.POST.get("address")
        profile.dob = request.POST.get("dob") or None
        profile.gender = request.POST.get("gender")
        profile.current_skills = request.POST.get("current_skills")
        profile.current_job = request.POST.get("current_job")
        profile.current_salary = request.POST.get("current_salary")
        profile.dream_role = request.POST.get("dream_role")

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("my_profile")

    return render(request, "my_profile.html", {"profile": profile})