from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),

    # Auth
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),

    # Dashboard (protected)
    path('dashboard/', views.dashboard, name="dashboard"),
]
