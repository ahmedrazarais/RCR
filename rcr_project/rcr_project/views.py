from django.http import HttpResponse
from django.shortcuts import render
from TeacherArea.models import Class, FileUpload,Assignment,StudentSubmission,Message
from StudentArea.models import StudentProfile,Enrollment



def home_rcr(request):
    if request.user.is_authenticated:  # Check if the user is logged in
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
            
            return render(request,"TeacherArea/teacher_home.html",context)
        
        else:
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


            return render(request,"StudentArea/student_home.html",context)
            
    else:
        return render(request,"rcr_home.html")


def about_rcr(request):
    return render(request,"rcr_about.html")


