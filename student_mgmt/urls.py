from django.contrib import admin
from django.urls import path, include
from student_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student_app.urls')),  # 👈 include your app’s URLs here
    path('students/', views.student_list, name='student_list'),

]
