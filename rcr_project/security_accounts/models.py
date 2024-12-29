from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Extends Django's AbstractUser to include additional fields such as status,
    email, and recovery_email, which are necessary for both Teacher and Student users.
    """
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    
    # Make email unique
    email = models.EmailField(unique=True)
    recovery_email = models.EmailField(unique=True, null=True, blank=True)  # Optional recovery email
    status = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')

    # Avoid reverse accessor conflict by changing related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Custom related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Custom related_name
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.status})"



class TeacherProfile(models.Model):
    """
    Profile model for Teachers, extending the User model with specific fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    
    def __str__(self):
        return f"Teacher: {self.user.username}"


class StudentProfile(models.Model):
    """
    Profile model for Students, extending the User model with specific fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    section = models.CharField(max_length=20, blank=False)
    roll_number = models.CharField(max_length=20, unique=True, blank=False)

    def __str__(self):
        return f"Student: {self.user.username} - Section: {self.section} - Roll No: {self.roll_number}"
