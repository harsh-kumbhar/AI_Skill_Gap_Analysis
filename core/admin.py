# core/admin.py
from django.contrib import admin
from .models import DreamRole,Skill,Profile

@admin.register(DreamRole)
class DreamRoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("skills",)  # better UI for M2M


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'dream_role', 'current_job')
    search_fields = ('user__username', 'dream_role__name')
    list_filter = ('dream_role',)