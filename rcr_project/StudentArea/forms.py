# forms.py
from django import forms
from TeacherArea.models import Class

class JoinClassForm(forms.Form):
    class_id = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a class'}),
        label="Select a Class"
    )
    class_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Class Code'}),
        label="Enter Class Code"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the class choices dynamically
        self.fields['class_id'].choices = [(class_obj.id, f"{class_obj.course_name} - {class_obj.department_name}") for class_obj in Class.objects.all()]















# forms.py
from django import forms
from TeacherArea.models import Message
from security_accounts.models import TeacherProfile

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']  # Only receiver and content fields

    def __init__(self, *args, **kwargs):
        student_profile = kwargs.pop('student_profile', None)
        super(MessageForm, self).__init__(*args, **kwargs)

        if student_profile:
            teacher_ids = student_profile.enrollments.values_list('class_obj__teacher', flat=True).distinct()
            self.fields['receiver'].queryset = TeacherProfile.objects.filter(id__in=teacher_ids)
