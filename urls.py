from django.contrib import admin
from django.urls import path, include
from student_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path('students/', include('student_app.urls')),
    path('attendance/', include('attendance_app.urls')),  
]
