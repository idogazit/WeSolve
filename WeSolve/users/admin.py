from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, Course, Faculty, School
from users.forms import CustomUserForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserForm
    model = CustomUser
    list_display = ["username", "email", "is_staff", "userId"]
    fieldsets = UserAdmin.fieldsets + (
        ('User info', {'fields': ('courses', 'rank', 'userPic', 'isTeacher')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email', 'courses', 'rank', 'userPic', 'isTeacher')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(School)