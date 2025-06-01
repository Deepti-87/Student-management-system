from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.http import HttpResponse
import csv
from .models import Attendance
from .forms import AttendanceForm
import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from .models import Grade
from .forms import GradeForm
from .models import Message
from .forms import MessageForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.db.models import Avg

def reports_view(request):
    students = Student.objects.all()
    attendance_summary = Attendance.objects.values('student').annotate(total=Count('id'))
    grades = Grade.objects.all()

    context = {
        'students': students,
        'attendance_summary': attendance_summary,
        'grades': grades,
    }
    return render(request, 'student_app/reports.html', context)


def grade_summary_report(request):
    summary = (
        Grade.objects
        .values('subject__name')
        .annotate(avg_score=Avg('score'))
    )

    subjects = [item['subject__name'] for item in summary]
    averages = [item['avg_score'] for item in summary]

    return render(request, 'student_app/grade_summary_report.html', {
        'summary': summary,
        'subjects': subjects,
        'averages': averages,
    })

def attendance_report(request):
    attendance_summary = Attendance.objects.values('student__name').annotate(
        present_days=Count('status', filter=models.Q(status='Present')),
        absent_days=Count('status', filter=models.Q(status='Absent'))
    )
    return render(request, 'student_app/attendance_report.html', {
        'attendance_summary': attendance_summary
    })


def attendance_report(request):
    students = Student.objects.all()
    report_data = []

    for student in students:
        total_present = Attendance.objects.filter(student=student, status='Present').count()
        total_absent = Attendance.objects.filter(student=student, status='Absent').count()
        total_days = total_present + total_absent

        if total_days > 0:
            attendance_percentage = (total_present / total_days) * 100
        else:
            attendance_percentage = 0

        report_data.append({
            'student': student,
            'present': total_present,
            'absent': total_absent,
            'percentage': round(attendance_percentage, 2)
        })

    return render(request, 'reports/attendance_report.html', {'report_data': report_data})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_app/student_list.html', {'students': students})

def is_teacher(user):
    return user.role == 'teacher'

def is_student(user):
    return user.role == 'student'

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, 'student_app/teacher_dashboard.html')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    return render(request, 'student_app/student_dashboard.html')


def send_message(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.student = student
            message.save()
            return redirect('student_notifications', student_id=student.id)
    else:
        form = MessageForm()

    return render(request, 'student_app/send_message.html', {
        'student': student,
        'form': form,
    })

def student_notifications(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    messages = student.messages.order_by('-created_at')

    
    messages.filter(read=False).update(read=True)

    return render(request, 'student_app/student_notifications.html', {
        'student': student,
        'messages': messages
    })
def home(request):
    return render(request, 'home.html')

def home(request):
    recent_messages = Message.objects.order_by('-created_at')[:5]
    return render(request, 'student_app/home.html', {'recent_messages': recent_messages})
def send_message(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.student = student
            message.save()

            # ✅ Send email notification
            send_mail(
                subject=f"New Message: {message.subject}",
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[student.email],
                fail_silently=False,
            )

            return redirect('student_notifications', student_id=student.id)
    else:
        form = MessageForm()

    return render(request, 'student_app/send_message.html', {
        'student': student,
        'form': form,
    })

def message_list(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'student_app/message_list.html', {'messages': messages})

def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'student_app/grade_list.html', {'grades': grades})

def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'student_app/grade_form.html', {'form': form})

def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'student_app/grade_form.html', {'form': form})

def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grade_list')
    return render(request, 'student_app/confirm_delete.html', {'object': grade})


def home(request):
    return render(request, 'home.html')


def export_students_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Students"

    # Header row
    ws.append(['Name', 'Email', 'Phone'])

    # Data rows
    for student in Student.objects.all():
        ws.append([student.name, student.email, student.email])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'
    wb.save(response)
    return response

def export_students_csv(request):
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(name__icontains=query) | Student.objects.filter(email__icontains=query)
    else:
        students = Student.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Enrollment Date'])

    for student in students:
        writer.writerow([student.name, student.email, student.enrollment_date])

    return response
# List students (with optional search)

def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        students = Student.objects.all()
    return render(request, 'student_app/student_list.html', {'students': students})

# Create new student
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # Make sure this name matches your URL
    else:
        form = StudentForm()
    return render(request, 'student_app/student_form.html', {'form': form})

# Edit student
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_app/student_form.html', {'form': form})

# Delete student
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_app/student_confirm_delete.html', {'student': student})

# ✅ Export to CSV
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Enrollment Date'])

    for student in Student.objects.all():
        writer.writerow([student.name, student.email, student.enrollment_date])

    return response


def attendance_list(request):
    attendance_records = Attendance.objects.all()
    context = {'attendance_records': attendance_records}
    return render(request, 'student_app/attendance_list.html', context)

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance_form.html', {'form': form})

