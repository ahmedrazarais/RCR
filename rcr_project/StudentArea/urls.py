
from django.urls import path,include
from . import views

urlpatterns = [
  
    path("" , views.student_home , name="student_home"),
    path("join_class/" ,views.join_class , name="join_class"),
    path('enrolled-classes/', views.student_enrolled_classes, name='enrolled_classes'),
    path('class/<int:class_id>/', views.class_content, name='class_content'),
    path('assignments/', views.list_assignments, name='list_assignments'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('send-message/', views.send_message, name='send_message'),
    
    
]