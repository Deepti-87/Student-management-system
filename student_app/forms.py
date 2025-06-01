from django import forms
from .models import Attendance
from .models import Student
from .models import Student, Grade 
from .models import Message 
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score']
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['student', 'subject', 'body']
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']