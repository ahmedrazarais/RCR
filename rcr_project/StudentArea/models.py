# models.py
from django.db import models
from security_accounts.models import StudentProfile
from TeacherArea.models import Class


class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='student_enrollments')  # Unique related_name
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.class_obj.course_name}"
