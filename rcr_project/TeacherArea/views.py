from django.shortcuts import render,redirect
from .forms import ClassForm,FileUploadForm,Announcement
from .models import Class,FileUpload
from django.shortcuts import get_object_or_404
from .forms import AnnouncementForm
from .models import Announcement
from .models import Class, FileUpload, Announcement
from .models import Class, Assignment, FileUpload, Announcement,StudentSubmission,Message
from .forms import AssignmentForm


from django.contrib import messages



# # Create your views here.
def teacher_home(request):
        current_user = request.user
        current_status=current_user.status

        if current_status=="teacher":
            total_classes = Class.objects.filter(teacher=current_user.teacher_profile).count()
            total_files_uploaded = FileUpload.objects.filter(teacher=current_user.teacher_profile).count()
            total_assignments = Assignment.objects.filter(teacher=current_user.teacher_profile).count()

            context = {
                'total_classes': total_classes,
                'total_assignments': total_assignments,
                'total_files_uploaded': total_files_uploaded,
            }
            
        return render(request , "TeacherArea/teacher_home.html",context)










def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            # Set the teacher field to the logged-in teacher
            class_instance = form.save(commit=False)  # Don't save yet
            class_instance.teacher = request.user.teacher_profile  # Set the teacher's profile
            class_instance.save()  # Save the class data to the database
            messages.success(request,"Class Has been created successfully.")
            return redirect('teacher_home')  # Redirect to a success page or class list
    else:
        form = ClassForm()

    return render(request, 'TeacherArea/create_class.html', {'form': form})




def view_classes(request):
    """
    Fetch all classes for the logged-in teacher and send to the template.
    """
    # Get the logged-in user's teacher profile
    teacher_profile = request.user.teacher_profile

    # Fetch all classes associated with this teacher
    classes = Class.objects.filter(teacher=teacher_profile)

    # Pass classes to the template
    return render(request, 'TeacherArea/view_classes.html', {'classes': classes})




def upload_file(request):
    if not request.user.is_authenticated:
        return redirect('rcr_home')

    teacher = request.user.teacher_profile
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES, teacher=teacher)
        if form.is_valid():
            file_upload = form.save(commit=False)
            file_upload.teacher = teacher
            file_upload.save()
            messages.success(request, "File uploaded successfully.")
            return redirect('teacher_home')  # Redirect after successful upload
    else:
        form = FileUploadForm(teacher=teacher)

    return render(request, 'TeacherArea/upload_file.html', {'form': form})







def class_detail(request, class_id):
    # Fetch the class object
    class_obj = get_object_or_404(Class, id=class_id)

    # Fetch related data
    files = FileUpload.objects.filter(class_obj=class_obj)
    announcements = Announcement.objects.filter(class_obj=class_obj)
    assignments = Assignment.objects.filter(class_obj=class_obj)  # Fetch assignments for this class

    context = {
        'class': class_obj,
        'files': files,
        'announcements': announcements,
        'assignments': assignments,  # Add assignments to the context
    }
    return render(request, 'TeacherArea/class_detail.html', context)







def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(teacher=request.user.teacher_profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)  # Do not save to the database yet
            assignment.teacher = request.user.teacher_profile  # Set the teacher field explicitly
            assignment.save()  # Save to the database
            messages.success(request, "Assignment uploaded successfully.")
            
            return redirect('teacher_home')  # Redirect to the teacher's dashboard or assignments page
    else:
        form = AssignmentForm(teacher=request.user.teacher_profile)

    return render(request, 'TeacherArea/upload_assignment.html', {'form': form})






def make_announcement(request):
    teacher = request.user.teacher_profile  # Assuming the logged-in user has a related teacher profile
    
    if request.method == "POST":
        # Pass teacher as a keyword argument when initializing the form
        form = AnnouncementForm(teacher=teacher, data=request.POST)
        
        if form.is_valid():
            # Set the teacher field manually if it's missing
            announcement = form.save(commit=False)
            announcement.teacher = teacher  # Ensure the teacher is set
            announcement.save()  # Save the announcement with the teacher assigned
            
            messages.success(request, "Announcement created successfully.")
            return redirect('teacher_home')  # Replace with the actual success URL
    else:
        # Pass teacher as a keyword argument for GET requests
        form = AnnouncementForm(teacher=teacher)

    return render(request, 'TeacherArea/make_announcement.html', {'form': form})





def view_submissions(request):
    teacher_classes = Class.objects.filter(teacher=request.user.teacher_profile)  # Assuming the teacher profile is linked to the user
    submissions = StudentSubmission.objects.filter(assignment__class_obj__in=teacher_classes)

    return render(request, 'TeacherArea/view_submissions.html', {'submissions': submissions})








from .models import Message



def teacher_messages(request):
    teacher = request.user.teacher_profile  # Assuming the teacher is logged in
    messages = Message.objects.filter(receiver=teacher)  # Remove ordering
    return render(request, 'TeacherArea/messages.html', {'messages': messages})
