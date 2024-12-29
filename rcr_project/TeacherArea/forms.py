from django import forms
from .models import Class,FileUpload,Announcement

class ClassForm(forms.ModelForm):
    """
    Form for creating or updating a Class instance.
    """
    class Meta:
        model = Class
        fields = ['course_name', 'department_name', 'class_code', 'description']  # Include all necessary fields

    # You can add custom validation or field-specific logic here if needed
    def clean_class_code(self):
        class_code = self.cleaned_data['class_code']
        # Custom validation for class code if needed
        return class_code






class FileUploadForm(forms.ModelForm):
    class_obj = forms.ModelChoiceField(
        queryset=None,
        label="Select Class",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = FileUpload
        fields = ['class_obj', 'file', 'description']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['class_obj'].queryset = teacher.classes.all()







class AnnouncementForm(forms.ModelForm):
    class_obj = forms.ModelChoiceField(
        queryset=None,  # Placeholder; will be set in __init__
        label="Select Class",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Announcement
        fields = ['class_obj', 'title', 'content']

    def __init__(self, teacher=None, *args, **kwargs):
        """
        Initialize the form and filter the class_obj queryset to show only classes created by the logged-in teacher.
        """
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['class_obj'].queryset = Class.objects.filter(teacher=teacher)  # Filter by teacher





from django import forms
from .models import Assignment
from .models import Class

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['class_obj', 'title', 'description', 'due_date', 'file']
        
    def __init__(self, teacher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_obj'].queryset = Class.objects.filter(teacher=teacher)  # Only show classes of the logged-in teacher
