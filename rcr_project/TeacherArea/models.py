from django.db import models

# Create your models here.

# TeacherProfile and StudentProfile from Security_accounts app
from security_accounts.models import TeacherProfile, StudentProfile

class Class(models.Model):
    """
    Class model representing each class created by a teacher.
    """
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='classes')
    course_name = models.CharField(max_length=200)  # Name of the course
    department_name = models.CharField(max_length=100)  # Name of the department
    class_code = models.CharField(max_length=50, unique=True)  # Unique code for the class
    description = models.TextField(blank=True, null=True)  # Description of the class
    date_created = models.DateTimeField(auto_now_add=True)  # Date and time when the class was created
    
    def __str__(self):
        return f"{self.course_name} - {self.class_code}"


    

class FileUpload(models.Model):
    """
    Model for teachers to upload files related to their classes.
    """
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='uploaded_files')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='class_files/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded by {self.teacher.user.username}"





class Announcement(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="announcements")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.teacher.user.username}"



from django.db import models
from security_accounts.models import TeacherProfile
from .models import Class

class Assignment(models.Model):
    """
    Model for storing assignments uploaded by teachers.
    """
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='assignments')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    file = models.FileField(upload_to='assignments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.class_obj.course_name} ({self.due_date})"









class StudentSubmission(models.Model):
    """
    Model to store student submissions for assignments.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)  # Optional feedback from the teacher
    grade = models.CharField(max_length=10, blank=True, null=True)  # Optional grade field

    def __str__(self):
        return f"Submission by {self.student.user.username} for {self.assignment.title}"
















class Message(models.Model):
    sender = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)  # Add sender field
    receiver = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    content = models.TextField()
    class_associated = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)  # Optional

    def __str__(self):
        return f"Message from {self.sender.user.username} to {self.receiver.user.username}"
