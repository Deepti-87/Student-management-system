from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    enrollment_date = models.DateField(default=timezone.now)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.name
    # student_app/models.py


class Message(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.subject} to {self.student.name}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  
    score = models.DecimalField(max_digits=5, decimal_places=2)
