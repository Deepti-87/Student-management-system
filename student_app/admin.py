from django.contrib import admin
from .models import Attendance
from .models import Grade
from .models import Student, Message
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Grade)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'created_at')
    list_filter = ('created_at',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
