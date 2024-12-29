from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import JoinClassForm
from TeacherArea.models import Class,StudentSubmission,Message
from .models import Enrollment





# Create your views here.
def student_home(request):
            current_user = request.user
            current_status=current_user.status

            total_classes = Enrollment.objects.filter(student=current_user.student_profile).count()
            total_submissions = StudentSubmission.objects.filter(student=current_user.student_profile).count()
            message_count = Message.objects.filter(sender=current_user.student_profile).count()
            print(message_count)
            print(total_classes)
            print(total_submissions)
            context = {
                'total_classes': total_classes,
                'total_assignment': total_submissions,
                'message_send': message_count,
            }
            return render(request , "StudentArea/student_home.html",context)




def join_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            class_code = form.cleaned_data['class_code']
            
            try:
                selected_class = Class.objects.get(id=class_id)
                if selected_class.class_code == class_code:
                    # Check if already enrolled
                    if Enrollment.objects.filter(student=request.user.student_profile, class_obj=selected_class).exists():
                        messages.error(request, "You are already enrolled in this class.")
                    else:
                        # Enroll the student
                        Enrollment.objects.create(
                            student=request.user.student_profile,
                            class_obj=selected_class
                        )
                        messages.success(request, f"You have successfully joined the class: {selected_class.course_name}.")
                        return redirect("student_home")  # Redirect to the student's dashboard
                else:
                    form.add_error('class_code', 'Invalid class code. Please try again.')
            except Class.DoesNotExist:
                form.add_error('class_id', 'Class not found. Please try again.')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JoinClassForm()

    return render(request, 'StudentArea/join_class.html', {'form': form})



# View to display all classes the student is enrolled in
def student_enrolled_classes(request):
    # Get the enrolled classes for the current logged-in student
    enrolled_classes = Enrollment.objects.filter(student=request.user.student_profile)

    # Fetch the class details for those enrolled classes
    classes = [enrollment.class_obj for enrollment in enrolled_classes]

    return render(request, 'StudentArea/enrolled_classes.html', {'classes': classes})




from TeacherArea.models import FileUpload, Assignment, Announcement


def class_content(request, class_id):
    # Get the class by its ID
    selected_class = get_object_or_404(Class, id=class_id)

    # Fetch the uploaded files, assignments, and announcements for this class
    files = FileUpload.objects.filter(class_obj=selected_class)
    assignments = Assignment.objects.filter(class_obj=selected_class)
    announcements = Announcement.objects.filter(class_obj=selected_class)

    # Render the class content page, passing the class content to the template
    return render(request, 'StudentArea/class_content.html', {
        'class': selected_class,
        'files': files,
        'assignments': assignments,
        'announcements': announcements,
    })








def list_assignments(request):
    student = request.user.student_profile
    # Get all classes the student is enrolled in
    enrollments = Enrollment.objects.filter(student=student)
    classes = [enrollment.class_obj for enrollment in enrollments]
    
    # Fetch assignments for these classes
    assignments = Assignment.objects.filter(class_obj__in=classes).order_by('-due_date')
    
    return render(request, 'StudentArea/assignments.html', {'assignments': assignments})





def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student_profile

    # Ensure the student is enrolled in the class
    if not Enrollment.objects.filter(student=student, class_obj=assignment.class_obj).exists():
        return render(request, 'student/error.html', {'message': 'You are not enrolled in this class.'})

    # Check if submission already exists
    submission = StudentSubmission.objects.filter(student=student, assignment=assignment).first()

    if request.method == 'POST' and not submission:
        file = request.FILES['file']
        StudentSubmission.objects.create(student=student, assignment=assignment, file=file)
        return redirect('assignment_detail', assignment_id=assignment.id)

    return render(request, 'StudentArea/assignment_detail.html', {
        'assignment': assignment,
        'submission': submission,
    })




from .forms import MessageForm

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, student_profile=request.user.student_profile)
        if form.is_valid():
            # Set the sender before saving the message
            message = form.save(commit=False)  # Don't save yet
            message.sender = request.user.student_profile  # Set the sender
            message.save()  # Now save it
            messages.success(request, 'Your message has been sent!')
            return redirect('student_home')  # Redirect to success page
        else:
            messages.error(request, 'There was an error in your form.')
    else:
        form = MessageForm(student_profile=request.user.student_profile)

    return render(request, 'StudentArea/send_message.html', {'form': form})
