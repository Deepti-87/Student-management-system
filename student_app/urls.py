from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('export_excel/', views.export_students_excel, name='export_students_excel'),
    path('export/csv/', views.export_students_csv, name='export_students_csv'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/add/', views.add_grade, name='add_grade'),
    path('grades/edit/<int:pk>/', views.edit_grade, name='edit_grade'),
    path('grades/delete/<int:pk>/', views.delete_grade, name='delete_grade'),
    path('send-message/', views.send_message, name='send_message'),
    path('messages/', views.message_list, name='message_list'),
    path('students/<int:student_id>/notifications/', views.student_notifications, name='student_notifications'),
    path('students/<int:student_id>/send_message/', views.send_message, name='send_message'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('reports/attendance/', views.attendance_report, name='attendance_report'),
    path('', views.home, name='home'),
    path('reports/grades/', views.grade_summary_report, name='grade_summary_report'),
    path('reports/', views.reports_view, name='reports'),

]

