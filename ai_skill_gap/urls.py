from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),

    # Auth
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),

    # Dashboard (protected)
    path('dashboard/', views.dashboard, name="dashboard"),
    path("my_profile/", views.my_profile, name="my_profile"),

    path("skill_analysis/", views.skill_analysis, name="skill_analysis"),
    path("resume_analyzer/", views.resume_analyzer, name="resume_analyzer"),  
    path("course-recommendations/", views.course_recommendations, name="course_recommendations"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
