from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Skill,DreamRole

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

                # ✅ Correct dream_role assignment
        dream_role_id = request.POST.get("dream_role")
        if dream_role_id:
            profile.dream_role_id = dream_role_id
        else:
            profile.dream_role = None


        # ✅ Skills handling (IDs + new skill names)
        selected_skills = request.POST.getlist("skills[]")
        skill_objs = []
        for val in selected_skills:
            if val.isdigit():
                skill = Skill.objects.filter(id=int(val)).first()
            else:
                skill, _ = Skill.objects.get_or_create(name=val)
            if skill:
                skill_objs.append(skill)

        profile.skills.set(skill_objs)

        profile.current_job = request.POST.get("current_job")
        profile.current_salary = request.POST.get("current_salary")


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
        "all_skills": Skill.objects.all(),
        "all_dream_roles": DreamRole.objects.all()  # 👈 send dream jobs
    })


@login_required(login_url='login')
def skill_analysis(request):
    profile = request.user.profile
    dream_role = profile.dream_role

    # Fetch current user skills
    user_skills = list(profile.skills.values_list("name", flat=True))

    # Fetch dream role required skills
    dream_role_skills = list(dream_role.skills.values_list("name", flat=True)) if dream_role else []

    # Skill matching logic
    matched_skills = [skill for skill in user_skills if skill in dream_role_skills]
    missing_skills = [skill for skill in dream_role_skills if skill not in user_skills]

    # (Optional) Recommend related skills for improvement — can be static or ML-based later
    # Example: based on missing skills, recommend similar or complementary skills
    recommendations = []
    if "Python" in missing_skills:
        recommendations.append("Learn Django or Flask for backend dev")
    if "Machine Learning" in missing_skills:
        recommendations.append("Explore TensorFlow or Scikit-learn")
    if "Communication" in missing_skills:
        recommendations.append("Practice with public speaking or presentation tools")

    context = {
        "profile": profile,
        "dream_role": dream_role,
        "user_skills": user_skills,
        "dream_role_skills": dream_role_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
    }

    return render(request, "skill_analysis.html", context)
