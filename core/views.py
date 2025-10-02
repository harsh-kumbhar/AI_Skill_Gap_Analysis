from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Skill

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
        # Profile auto-created via signals.py
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
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')


# Logout View
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        "profile": profile
    }
    return render(request, "dashboard.html", context)

@login_required(login_url='login')
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.address = request.POST.get("address")
        profile.dob = request.POST.get("dob") or None
        profile.gender = request.POST.get("gender")

        # ✅ Skills handling (IDs + new skill names)
        selected_skills = request.POST.getlist("skills[]")
        skill_objs = []
        for val in selected_skills:
            if val.isdigit():
                # existing skill (ID)
                skill = Skill.objects.filter(id=int(val)).first()
            else:
                # new skill (name)
                skill, _ = Skill.objects.get_or_create(name=val)
            if skill:
                skill_objs.append(skill)

        profile.skills.set(skill_objs)

        profile.current_job = request.POST.get("current_job")
        profile.current_salary = request.POST.get("current_salary")
        profile.dream_role = request.POST.get("dream_role")

        # Resume file upload
        if request.FILES.get("resume"):
            profile.resume = request.FILES["resume"]

        # Profile Picture upload
        if request.FILES.get("profile_pic"):
            profile.profile_pic = request.FILES["profile_pic"]

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("my_profile")

    return render(request, "my_profile.html", {
        "profile": profile,
        "all_skills": Skill.objects.all()
    })
